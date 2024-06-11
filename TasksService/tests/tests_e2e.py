import pytest
import grpc
from unittest.mock import patch
from testcontainers.postgres import PostgresContainer
from sqlalchemy.ext.asyncio import create_async_engine

from tasks_service.routers import TaskService
from common.proto import tasks_pb2, tasks_pb2_grpc
from database.session import init_models
from utils.model_repository import get_task_repo

@pytest.fixture(scope="module")
def postgres_container():
    container = PostgresContainer("postgres:latest")
    container.start()
    yield container
    container.stop()

@pytest.fixture(scope="module")
async def stub(postgres_container):
    with patch("database.session.get_engine") as mock_get_engine:
        uri = postgres_container.get_connection_url().replace("postgresql+psycopg2://", "postgresql+asyncpg://")
        mock_get_engine.return_value = create_async_engine(uri, echo=True)

        await init_models()

        servicer = TaskService()
        server = grpc.aio.server()
        tasks_pb2_grpc.add_TaskServiceServicer_to_server(servicer, server)
        port = server.add_insecure_port("[::]:50052")
        await server.start()

        async with grpc.aio.insecure_channel(f"localhost:{port}") as channel:
            yield tasks_pb2_grpc.TaskServiceStub(channel)

        await server.stop(0)

@pytest.fixture(scope="module")
def task_repo(stub):
    return get_task_repo()


@pytest.mark.asyncio
async def test_create_task(stub, task_repo):
    async for client in stub:
        request = tasks_pb2.CreateTaskRequest(title="Test Task", text="Test Text", author="Author1")
        response = await client.CreateTask(request)
        assert response.title == "Test Task"
        assert response.text == "Test Text"
        assert response.author == "Author1"

        request = tasks_pb2.GetTaskByIdRequest(task_id=response.task_id)
        response = await client.GetTaskById(request)
        assert response.title == "Test Task"
        assert response.text == "Test Text"
