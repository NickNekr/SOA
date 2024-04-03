import grpc

from config import get_config
from common.proto import tasks_pb2_grpc

config = get_config()

async def get_stub():
    async with grpc.aio.insecure_channel(f'{config.Grpc.HOST}:{config.Grpc.PORT}') as channel:
        stub = tasks_pb2_grpc.TaskServiceStub(channel)
        yield stub
