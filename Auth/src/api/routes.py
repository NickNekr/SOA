from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from contextlib import asynccontextmanager

from api.endpoints.auth import auth_router
from api.endpoints.tasks import tasks_router
from api.endpoints.stats import stats_router
from database.session import init_models
from message_broker.producer import get_producer

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_models()
    producer = get_producer()
    await producer.start()

    yield

    await producer.stop()

app = FastAPI(lifespan=lifespan)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={"detail": "Validations error", "errors": exc.errors()},
    )

app.include_router(auth_router, tags=["auth"])
app.include_router(tasks_router, tags=["tasks"])
app.include_router(stats_router, tags=["stats"])
