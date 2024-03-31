import uvicorn
import asyncio

from api.routes import app
from config import get_config


if __name__ == "__main__":
    app_config = get_config()
    uvicorn.run(app, host=app_config.FastApi.HOST, port=app_config.FastApi.PORT)
