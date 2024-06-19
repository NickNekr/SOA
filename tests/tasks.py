import pytest
import grpc

from common.tasks_proto import tasks_pb2_grpc
from TasksService.src.tasks_service.routers import TaskService
from TasksService.src.database.session import init_models
from TasksService.src.config import get_config

from tests.conftest import Config

@pytest.fixture
def app_config_tasks():
    yield get_config()


@pytest.fixture
async def tasks_server(config_patch_tasks):
    await init_models()

    servicer = TaskService()
    server = grpc.aio.server()
    tasks_pb2_grpc.add_TaskServiceServicer_to_server(servicer, server)
    port = server.add_insecure_port(f"[::]:{Config.TASKS_PORT}")
    await server.start()

    yield server

    await server.stop(0)
