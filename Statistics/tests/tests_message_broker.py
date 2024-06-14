import pytest
import asyncio
import grpc
import pickle
from unittest.mock import patch
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from testcontainers.postgres import PostgresContainer
from testcontainers.kafka import KafkaContainer
from fastapi.testclient import TestClient

from api.routes import app
from config import get_config
from database.session import init_models
from statistics_service.statistics import StatisticsService
from common.statistics_proto import statistics_pb2_grpc
from common.statistics_proto import statistics_pb2
from database.session import init_models, get_session_outside_depends
from database.model import Likes, Views
from tools.repo_alchemy_linker import MonoRepos, get_mono_repos
from run import lifespan

@pytest.fixture
def task_id():
    return "d160b410-e6a8-4cbb-92c2-068112187503"

@pytest.fixture
def kafka_container():
    with KafkaContainer("confluentinc/cp-kafka:7.6.0") as container:
        container.start()
        yield container

@pytest.fixture
async def postgres_container():
    with PostgresContainer("postgres:latest") as container:
        container.start()
        yield container

@pytest.fixture
def config_patch(kafka_container, postgres_container):
    app_config = get_config()

    host, port = kafka_container.get_bootstrap_server().split(":")

    app_config.Kafka.KAFKA_HOST = host
    app_config.Kafka.KAFKA_PORT = port

    uri = postgres_container.get_connection_url().replace("postgresql+psycopg2://", "postgresql+asyncpg://")
    app_config.DataBase.SQLALCHEMY_DATABASE_URI = uri


    with patch("config.get_config", return_value=app_config):
        yield app_config

@pytest.fixture
async def producer(config_patch):
    producer = AIOKafkaProducer(bootstrap_servers=f"{config_patch.Kafka.KAFKA_HOST}:{config_patch.Kafka.KAFKA_PORT}")
    await producer.start()
    yield producer
    await producer.stop()

@pytest.fixture
async def stub(config_patch):
    async with lifespan():
        servicer = StatisticsService()
        server = grpc.aio.server()
        statistics_pb2_grpc.add_StatisticsServiceServicer_to_server(servicer, server)
        port = server.add_insecure_port("[::]:50052")
        await server.start()

        async with grpc.aio.insecure_channel(f"localhost:{port}") as channel:
            yield statistics_pb2_grpc.StatisticsServiceStub(channel)

        await server.stop(0)

@pytest.mark.asyncio
async def test_produce_and_consume(producer, stub, config_patch, task_id):
    msg = {"task_id": task_id, "username": "Nik", "author": "Nik"}
    data = pickle.dumps(msg)

    await producer.send(topic=config_patch.Kafka.CONSUMER_TOPIC_LIKES, value=data)
    await asyncio.sleep(1)

    request = statistics_pb2.TaskRequest(task_id=task_id)
    response = await stub.GetTaskStats(request)
    assert response.task_id == task_id
    assert response.likes == 1
    assert response.views == 0
