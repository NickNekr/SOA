from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from api.endpoints.auth import auth_router
from database.session import init_models

app = FastAPI()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={"detail": "Validations error", "errors": exc.errors()},
    )

app.include_router(auth_router, tags=["auth"])
app.add_event_handler("startup", init_models)