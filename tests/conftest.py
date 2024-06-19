import pytest
from unittest.mock import patch
from testcontainers.postgres import PostgresContainer
from testcontainers.kafka import KafkaContainer

from tests.common import *


@pytest.fixture
async def postgres_container():
    with PostgresContainer("postgres:latest") as container:
        yield container


@pytest.fixture
def kafka_container():
    with KafkaContainer("confluentinc/cp-kafka:7.6.0") as container:
        container.start()
        yield container

@pytest.fixture
def config_patch_statistics(kafka_container, postgres_container, app_config_statistics):
    with patch("Statistics.src.config.get_config", return_value=app_config_statistics):
        change_kafka_config(kafka_container, app_config_statistics)
        change_postgres_config(postgres_container, app_config_statistics)
        yield app_config_statistics


@pytest.fixture
def config_patch_auth(kafka_container, postgres_container, app_config_auth):
    with patch("Auth.src.config.get_config", return_value=app_config_auth):
        change_kafka_config(kafka_container, app_config_auth)
        change_postgres_config(postgres_container, app_config_auth)
        change_grpc_config(app_config_auth)
        yield app_config_auth

@pytest.fixture
def config_patch_tasks(postgres_container, app_config_tasks):
    with patch("TasksService.src.config.get_config", return_value=app_config_tasks):
        change_postgres_config(postgres_container, app_config_tasks)
        yield app_config_tasks