import pytest
import grpc

from common.statistics_proto import statistics_pb2_grpc
from Statistics.src.statistics_service.statistics import StatisticsService
from Statistics.src.config import get_config
from Statistics.src.database.session import init_models
from Statistics.src.run import lifespan

from tests.conftest import Config


@pytest.fixture
def app_config_statistics():
    yield get_config()

@pytest.fixture
async def statistics_server(config_patch_statistics):
    async with lifespan():
        await init_models()

        servicer = StatisticsService()
        server = grpc.aio.server()
        statistics_pb2_grpc.add_StatisticsServiceServicer_to_server(servicer, server)
        port = server.add_insecure_port(f"[::]:{Config.STAT_PORT}")
        await server.start()

        yield server

        await server.stop(0)
