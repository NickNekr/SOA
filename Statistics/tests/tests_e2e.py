import pytest
import grpc
import pickle
from unittest.mock import patch
from testcontainers.postgres import PostgresContainer
from sqlalchemy.ext.asyncio import create_async_engine

from common.statistics_proto import statistics_pb2_grpc
from common.statistics_proto import statistics_pb2
from Statistics.src.statistics_service.statistics import StatisticsService
from Statistics.src.database.session import init_models
from Statistics.src.database.model import Likes, Views
from Statistics.src.tools.repo_alchemy_linker import MonoRepos, get_mono_repos

@pytest.fixture
def task_id():
    return "d160b410-e6a8-4cbb-92c2-068112187503"


class MessageDataTest:
    def __init__(self, msg) -> None:
        self.value = msg

@pytest.fixture
def postgres_container():
    with PostgresContainer("postgres:latest") as container:
        container.start()
        yield container

@pytest.fixture
async def engine_patch(postgres_container):
    uri = postgres_container.get_connection_url().replace("postgresql+psycopg2://", "postgresql+asyncpg://")
    engine = create_async_engine(uri, echo=True)
    print(f"Created async engine with URI: {uri}")

    with patch("Statistics.src.database.session.get_engine", return_value=engine):
        await init_models()
        yield

@pytest.fixture
def mono_repo(engine_patch) -> MonoRepos:
    return get_mono_repos()

@pytest.fixture
async def stub(engine_patch, mono_repo, task_id):

    async def add_data():
        data = {"task_id": task_id, "username": "test", "author": "Nik"}
        msg = pickle.dumps(data)

        await mono_repo.ProduceEntity(MessageDataTest(msg), Likes)
        await mono_repo.ProduceEntity(MessageDataTest(msg), Views)

    await init_models()
    await add_data()
    

    servicer = StatisticsService()
    server = grpc.aio.server()
    statistics_pb2_grpc.add_StatisticsServiceServicer_to_server(servicer, server)
    port = server.add_insecure_port("[::]:50052")
    await server.start()

    async with grpc.aio.insecure_channel(f"localhost:{port}") as channel:
        yield statistics_pb2_grpc.StatisticsServiceStub(channel)

    await server.stop(0)


@pytest.mark.asyncio
async def test_create_task(stub, task_id):
    request = statistics_pb2.TaskRequest(task_id=task_id)
    response = await stub.GetTaskStats(request)
    assert response.task_id == task_id
    assert response.likes == 1
    assert response.views == 1