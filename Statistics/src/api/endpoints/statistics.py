from fastapi import APIRouter

from config import get_config

app_config = get_config()

statistics_router = APIRouter(prefix="/statistics")

@statistics_router.get("/health")
async def authenticate():
    return 200