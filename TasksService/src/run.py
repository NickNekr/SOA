import logging
import asyncio

from TasksService.src.tasks_service.routers import server
from TasksService.src.database.session import init_models

async def run():
    await init_models()
    await server()

if __name__ == '__main__':
    logging.basicConfig()
    asyncio.run(run())
