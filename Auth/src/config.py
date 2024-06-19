from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
import os

class DataBaseConfig(BaseSettings):
    model_config = SettingsConfigDict(extra='ignore')

    DB_HOST: str = 'auth_service_db'
    DB_NAME: str = "auth_service"
    DB_USER: str = 'user'
    DB_PASSWORD: str = 'password'
    DB_PORT: int = 5432

    SQLALCHEMY_DATABASE_URI: str = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

class FastApiConfig(BaseSettings):
    model_config = SettingsConfigDict(extra='ignore')

    PORT: int = 8000
    HOST: str = "0.0.0.0"

    SECRET_KEY: str = "de1a0803f51423277838a8901a2ca930762de06d9993f3f129998828b521e719" # openssl rand -hex 32
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

class GrpcConfig(BaseSettings):
    model_config = SettingsConfigDict(extra='ignore')

    TASKS_PORT: int = 8001
    TASKS_HOST: str = "tasks"

    STAT_PORT: int = 8005
    STAT_HOST: str = "statistics"

class KafkaConfig(BaseSettings):
    model_config = SettingsConfigDict(extra='ignore')

    KAFKA_PORT: int = 29092
    KAFKA_HOST: str = "soa-kafka"

    PRODUCER_TOPIC_VIEWS: str = "views-post"
    PRODUCER_TOPIC_LIKES: str = "likes-post"


class Config(BaseSettings):
    env_file_: str = os.path.abspath(os.path.dirname(__file__)) + "/../" + os.environ.get("ENVIROMENT", ".env")

    model_config = SettingsConfigDict(env_file=env_file_, extra='ignore')

    FastApi: FastApiConfig = FastApiConfig(_env_file=env_file_)
    DataBase: DataBaseConfig = DataBaseConfig(_env_file=env_file_)
    Grpc: GrpcConfig = GrpcConfig(_env_file=env_file_)
    Kafka: KafkaConfig = KafkaConfig(_env_file=env_file_)

    ENV: str = "dev"


@lru_cache
def get_config():
    print("AUTH GET_CONFIG")
    return Config()
