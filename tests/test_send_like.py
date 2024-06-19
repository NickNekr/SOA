import pytest
from httpx import AsyncClient

from tests.statistics import *
from tests.auth import *
from tests.tasks import *
from tests.common import *

@pytest.mark.asyncio
async def test_send_likes(async_client: AsyncClient, statistics_server, tasks_server):
    await register_user(async_client)
    token = await auth_user(async_client)
    task_id = await create_task(async_client, token)
    await send_likes(async_client, task_id, token)
    await get_task_stat(async_client, task_id, token)