import pytest
from httpx import AsyncClient

from Auth.src.api.routes import app 
from Auth.src.config import get_config
from Auth.src.api.routes import lifespan

from tests.conftest import config_patch_auth

@pytest.fixture
def service():
    return "Auth"

@pytest.fixture
def app_config_auth():
    yield get_config()

@pytest.fixture
async def async_client(config_patch_auth):
    async with lifespan(app): 
        async with AsyncClient(app=app, base_url="http://testserver") as client:
            yield client


