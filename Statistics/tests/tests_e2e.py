import pytest
import pickle
import uuid
from unittest.mock import patch
from testcontainers.postgres import PostgresContainer
from sqlalchemy.ext.asyncio import create_async_engine

from database.session import init_models, get_engine
from src.tools.repo_alchemy_linker import get_mono_repos, MonoRepos
from database.model import Views, Likes
from database.session import get_session_outside_depends


class MessageDataTest:
    def __init__(self, msg) -> None:
        self.value = msg

@pytest.fixture
def postgres_container():
    container = PostgresContainer("postgres:latest")
    container.start()
    yield container
    container.stop()

@pytest.fixture
async def engine_patch(postgres_container):
    uri = postgres_container.get_connection_url().replace("postgresql+psycopg2://", "postgresql+asyncpg://")
    engine = create_async_engine(uri, echo=True)
    print(f"Created async engine with URI: {uri}")

    with patch("database.session.get_engine", return_value=engine):
        await init_models()
        yield

@pytest.fixture
def mono_repo(engine_patch) -> MonoRepos:
    return get_mono_repos()

@pytest.mark.asyncio
async def test_produce_entity(mono_repo):
    data = {"task_id": "d160b410-e6a8-4cbb-92c2-068112187503", "username": "test"}
    msg = pickle.dumps(data)

    for entity in (Likes, Views):
        await mono_repo.ProduceEntity(MessageDataTest(msg), entity)
        _, stats_repo, stats_entity = mono_repo.get_state(entity)
        async with get_session_outside_depends() as session:
            obj_stats = await stats_repo.get_by_condition((stats_entity.task_id == data["task_id"]), session)
            assert obj_stats is not None
            assert obj_stats.task_id == uuid.UUID(data["task_id"])
            assert obj_stats.count == 1

