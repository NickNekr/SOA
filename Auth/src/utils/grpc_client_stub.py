import grpc

from config import get_config
from common.tasks_proto import tasks_pb2_grpc
from common.statistics_proto import statistics_pb2_grpc

config = get_config()

async def get_tasks_stub():
    async with grpc.aio.insecure_channel(f'{config.Grpc.TASKS_HOST}:{config.Grpc.TASKS_PORT}') as channel:
        stub = tasks_pb2_grpc.TaskServiceStub(channel)
        yield stub

async def get_stat_stub():
    async with grpc.aio.insecure_channel(f'{config.Grpc.STAT_HOST}:{config.Grpc.STAT_PORT}') as channel:
        stub = statistics_pb2_grpc.StatisticsServiceStub(channel)
        yield stub