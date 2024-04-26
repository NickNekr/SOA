import logging
import asyncio

from tasks_service.routers import serve
from database.session import init_models

async def run():
    await init_models()
    await serve()

if __name__ == '__main__':
    logging.basicConfig()
    asyncio.run(run())
