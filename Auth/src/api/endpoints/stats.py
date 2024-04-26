from fastapi import APIRouter, Depends
from uuid import UUID

from utils.auth_utils import get_current_user
from message_broker.producer import get_producer, Producer
from database.model import User
from config import get_config


stats_router = APIRouter(prefix="/stats")

app_config = get_config()


@stats_router.post("/view/{task_id}")
async def send_view(
    task_id: UUID, 
    current_user: User = Depends(get_current_user),
    producer: Producer = Depends(get_producer)
):
    task_id = str(task_id)
    await producer.send_message({"task_id": task_id, "username": current_user.username}, app_config.Kafka.PRODUCER_TOPIC_VIEWS)
    return {"Message": "View was send!"}

@stats_router.post("/like/{task_id}")
async def send_view(
    task_id: UUID, 
    current_user: User = Depends(get_current_user),
    producer: Producer = Depends(get_producer)
):
    task_id = str(task_id)
    await producer.send_message({"task_id": task_id, "username": current_user.username}, app_config.Kafka.PRODUCER_TOPIC_LIKES)
    return {"Message": "Like was send!"}