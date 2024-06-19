from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from contextlib import asynccontextmanager
import asyncio

from Statistics.src.api.endpoints.statistics import statistics_router
from Statistics.src.database.session import init_models
from Statistics.src.message_broker.consumer import consume
from Statistics.src.message_broker.callback_functions import views_callback, likes_callback
from Statistics.src.config import get_config

app_config = get_config()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await asyncio.sleep(15)
    await init_models()
    views_task = asyncio.create_task(consume(app_config.Kafka.CONSUMER_TOPIC_VIEWS, views_callback))
    likes_task = asyncio.create_task(consume(app_config.Kafka.CONSUMER_TOPIC_LIKES, likes_callback))

    yield

    views_task.cancel()
    likes_task.cancel()

app = FastAPI(lifespan=lifespan)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={"detail": "Validations error", "errors": exc.errors()},
    )

app.include_router(statistics_router, tags=["statistics"])