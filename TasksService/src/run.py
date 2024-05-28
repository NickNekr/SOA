import logging
import asyncio

from tasks_service.routers import server
from database.session import init_models

async def run():
    await init_models()
    await server()

if __name__ == '__main__':
    logging.basicConfig()
    asyncio.run(run())
