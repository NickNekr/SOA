import pytest
import asyncio
import pickle
from unittest.mock import patch
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from testcontainers.postgres import PostgresContainer
from testcontainers.kafka import KafkaContainer
import pytest
from fastapi.testclient import TestClient
from api.routes import app
from config import get_config



@pytest.fixture
def kafka_container():
    with KafkaContainer("confluentinc/cp-kafka:7.6.0") as container:
        container.start()
        yield container

@pytest.fixture
def config_patch(kafka_container):
    app_config = get_config()
        KAFKA_HOST: str = kafka_container.get_container_host_ip()
        KAFKA_PORT: int = kafka_container.get_exposed_port(KAFKA_HOST)

        CONSUMER_TOPIC_VIEWS: str = "views-post"
        CONSUMER_TOPIC_LIKES: str = "likes-post"
    

    with patch("config.KafkaConfig", return_value=KafkaConfig):
        with patch("config.KafkaConfig", return_value=KafkaConfig):
            yield KafkaConfig

@pytest.fixture
async def postgres_container():
    with PostgresContainer("postgres:latest") as container:
        container.start()
        yield container

@pytest.fixture
async def producer(kafka_container):
    producer = AIOKafkaProducer(bootstrap_servers=kafka_container.get_bootstrap_server())
    await producer.start()
    yield producer
    await producer.stop()

@pytest.fixture
def client(config_patch):
    return TestClient(app)

@pytest.mark.asyncio
async def test_produce_and_consume(producer):
    msg = {"task_id": "d160b410-e6a8-4cbb-92c2-068112187503", "username": "test"}
    data = pickle.dumps(msg)

    print("HELLo")
    await producer.send_and_wait(topic="views-post", value=data)

    print("SENDED")

    # async for message in consumer:
    #     consume_data = pickle.loads(message.value)
    #     assert consume_data['task_id'] == msg['task_id']
    #     assert consume_data['username'] == msg['username']

    #     break
