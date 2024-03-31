from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
import os

class DataBaseConfig(BaseSettings):
    model_config = SettingsConfigDict(extra='ignore')

    DB_HOST: str = 'tasks_service_db'
    DB_NAME: str = "tasks_service"
    DB_USER: str = 'user'
    DB_PASSWORD: str = 'password'
    DB_PORT: int = 5432

    SQLALCHEMY_DATABASE_URI: str = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

class GrpcConfig(BaseSettings):
    model_config = SettingsConfigDict(extra='ignore')

    PORT: int = 8001
    HOST: str = "0.0.0.0"

class Config(BaseSettings):
    env_file_: str = os.path.abspath(os.path.dirname(__file__)) + "/../" + os.environ.get("ENVIROMENT", ".env")

    model_config = SettingsConfigDict(env_file=env_file_, extra='ignore')

    DataBase: DataBaseConfig = DataBaseConfig(_env_file=env_file_)
    Grpc: GrpcConfig = GrpcConfig(_env_file=env_file_)

    ENV: str = "dev"



    

@lru_cache
def get_config():
    return Config()
