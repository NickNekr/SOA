from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
import os

class DataBaseConfig(BaseSettings):
    model_config = SettingsConfigDict(extra='ignore')

    DB_HOST: str = 'statistics_service_db'
    DB_NAME: str = "statistics_service"
    DB_USER: str = 'user'
    DB_PASSWORD: str = 'password'
    DB_PORT: int = 5432

    SQLALCHEMY_DATABASE_URI: str = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

class FastApiConfig(BaseSettings):
    model_config = SettingsConfigDict(extra='ignore')

    PORT: int = 8002
    HOST: str = "0.0.0.0"

class KafkaConfig(BaseSettings):
    model_config = SettingsConfigDict(extra='ignore')

    KAFKA_PORT: int = 29092
    KAFKA_HOST: str = "soa-kafka"

    CONSUMER_TOPIC_VIEWS: str = "views-post"
    CONSUMER_TOPIC_LIKES: str = "likes-post"

class Config(BaseSettings):
    env_file_: str = os.path.abspath(os.path.dirname(__file__)) + "/../" + os.environ.get("ENVIROMENT", ".env")

    model_config = SettingsConfigDict(env_file=env_file_, extra='ignore')

    FastApi: FastApiConfig = FastApiConfig(_env_file=env_file_)
    DataBase: DataBaseConfig = DataBaseConfig(_env_file=env_file_)
    Kafka: KafkaConfig = KafkaConfig(_env_file=env_file_)

    ENV: str = "dev"

    

@lru_cache
def get_config():
    return Config()
