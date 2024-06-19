from httpx import AsyncClient
import asyncio

class Config:
    TASKS_PORT: int = 50052
    TASKS_HOST: str = "localhost"

    STAT_PORT: int = 50051
    STAT_HOST: str = "localhost"

def change_kafka_config(kafka_container, app_config):
    host, port = kafka_container.get_bootstrap_server().split(":")
    app_config.Kafka.KAFKA_HOST = host
    app_config.Kafka.KAFKA_PORT = port

def change_postgres_config(postgres_container, app_config):
    uri = postgres_container.get_connection_url().replace("postgresql+psycopg2://", "postgresql+asyncpg://")
    app_config.DataBase.SQLALCHEMY_DATABASE_URI = uri

def change_grpc_config(app_config):
    app_config.Grpc = Config()



async def register_user(client: AsyncClient):
    url = "/auth/register/"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }
    data = {
        "username": "string",
        "password": "string"
    }
    response = await client.post(url, headers=headers, json=data)
    
    assert response.status_code == 200
    return response

async def auth_user(client: AsyncClient):
    url = "/auth/"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "",
        "username": "string",
        "password": "string",
        "scope": "",
        "client_id": "",
        "client_secret": ""
    }

    response = await client.post(url, headers=headers, data=data)
    
    assert response.status_code == 200
    response_data = response.json()
    assert response_data is not None
    return response_data["access_token"]

async def create_task(client: AsyncClient, token: str):
    url = "/tasks/"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    data = {
        "title": "string",
        "text": "string"
    }

    response = await client.post(url, headers=headers, json=data)
    
    assert response.status_code == 200
    response_data = response.json()
    assert response_data is not None
    return response_data["task_id"]

async def send_likes(client: AsyncClient, task_id, token):
    url = f"/stats/like/{task_id}"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {token}"
    }

    response = await client.post(url, headers=headers)

    assert response.status_code == 200  
    assert response.json() is not None
    await asyncio.sleep(1)

async def get_task_stat(client: AsyncClient, task_id, token):
    url = f"/stats/task/{task_id}"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {token}",
    }

    response = await client.get(url, headers=headers)

    assert response.status_code == 200 
    response_data = response.json()
    assert response_data is not None
    assert response_data["task_id"] == task_id
    assert response_data["views"] == 0
    assert response_data["likes"] == 1