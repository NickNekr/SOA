import asyncio
import logging
from contextlib import asynccontextmanager

from config import get_config

from database.session import init_models
from message_broker.consumer import consume
from message_broker.callback_functions import views_callback, likes_callback
from config import get_config

from statistics_service.statistics import server
from database.session import init_models


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

# if __name__ == "__main__":
#     app_config = get_config()
#     uvicorn.run(app, host=app_config.FastApi.HOST, port=app_config.FastApi.PORT)
