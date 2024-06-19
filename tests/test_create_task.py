import pytest
from httpx import AsyncClient

from tests.statistics import *
from tests.auth import *
from tests.tasks import *
from tests.common import *


@pytest.mark.asyncio
async def test_create_task(async_client: AsyncClient, statistics_server, tasks_server):
    await register_user(async_client)
    token = await auth_user(async_client)
    await create_task(async_client, token)
