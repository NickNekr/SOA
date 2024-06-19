from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID
from grpc import RpcError, StatusCode

from common.tasks_proto import tasks_pb2
from common.statistics_proto import statistics_pb2
from common.schema import TaskStatsResponse, TopTasksResponse, TopUsersResponse
from Auth.src.utils.auth_utils import get_current_user
from Auth.src.utils.grpc_client_stub import get_tasks_stub, get_stat_stub
from Auth.src.message_broker.producer import get_producer, Producer
from Auth.src.database.model import User
from Auth.src.config import get_config


stats_router = APIRouter(prefix="/stats")

app_config = get_config()

async def get_author(
    task_id,
    stub
):
    try:
        ans = await stub.GetTaskById(tasks_pb2.GetTaskByIdRequest(task_id=task_id))
        return ans.author
    except RpcError as e:
        return None

async def make_grpc_request(
    request_message,
    grpc_method,
):
    try:
        return await grpc_method(request_message)
    except RpcError as e:
        if e.code() == StatusCode.NOT_FOUND:
            raise HTTPException(status_code=404, detail="Task not found")


@stats_router.get("/task/{task_id}", response_model=TaskStatsResponse)
async def get_task_stats(
    task_id: UUID, 
    current_user: User = Depends(get_current_user),
    stub = Depends(get_stat_stub),
):
    task_id = str(task_id)
    get_task_request = statistics_pb2.TaskRequest(task_id=task_id)
    return await make_grpc_request(get_task_request, stub.GetTaskStats)

@stats_router.get("/tasks/{sort_by}", response_model=TopTasksResponse)
async def get_top_tasks(
    sort_by: str, 
    current_user: User = Depends(get_current_user),
    stub = Depends(get_stat_stub),
):
    get_task_request = statistics_pb2.TopTasksRequest(sort_by=sort_by)
    return await make_grpc_request(get_task_request, stub.GetTopTasks)

@stats_router.get("/users", response_model=TopUsersResponse)
async def get_top_users(
    current_user: User = Depends(get_current_user),
    stub = Depends(get_stat_stub),
):
    get_task_request = statistics_pb2.TopUsersRequest()
    return await make_grpc_request(get_task_request, stub.GetTopUsers)

@stats_router.post("/view/{task_id}")
async def send_view(
    task_id: UUID, 
    current_user: User = Depends(get_current_user),
    producer: Producer = Depends(get_producer),
    stub = Depends(get_tasks_stub),
):
    task_id = str(task_id)
    author = await get_author(task_id, stub)
    await producer.send_message({"task_id": task_id, "username": current_user.username, "author": author}, app_config.Kafka.PRODUCER_TOPIC_VIEWS)
    return {"Message": "View was send!"}

@stats_router.post("/like/{task_id}")
async def send_like(
    task_id: UUID, 
    current_user: User = Depends(get_current_user),
    producer: Producer = Depends(get_producer),
    stub = Depends(get_tasks_stub),
):
    print("HELLO FROM LIKES")
    task_id = str(task_id)
    author = await get_author(task_id, stub)
    await producer.send_message({"task_id": task_id, "username": current_user.username, "author": author}, app_config.Kafka.PRODUCER_TOPIC_LIKES)
    return {"Message": "Like was send!"}