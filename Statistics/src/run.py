import asyncio
import logging
from contextlib import asynccontextmanager

from Statistics.src.message_broker.consumer import consume
from Statistics.src.message_broker.callback_functions import views_callback, likes_callback
from Statistics.src.statistics_service.statistics import server
from Statistics.src.database.session import init_models
from Statistics.src.config import get_config


@asynccontextmanager
async def lifespan():
    await asyncio.sleep(15)
    await init_models()

    app_config = get_config()
    views_task = asyncio.create_task(consume(app_config.Kafka.CONSUMER_TOPIC_VIEWS, views_callback))
    likes_task = asyncio.create_task(consume(app_config.Kafka.CONSUMER_TOPIC_LIKES, likes_callback))

    yield

    views_task.cancel()
    likes_task.cancel()

async def run():
    async with lifespan():
        await init_models()
        await server()

if __name__ == '__main__':
    logging.basicConfig()
    asyncio.run(run())