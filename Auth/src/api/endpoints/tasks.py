from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List
from database.session import get_session
from uuid import UUID
from grpc import RpcError
import grpc

from common.proto import tasks_pb2
from common.schema import TaskSchema, TaskIdSchema, DeleteTaskResponse, FullTaskSchema
from utils.auth_utils import get_current_user
from utils.grpc_client_stub import get_stub
from message_broker.producer import get_producer, Producer
from database.model import User
from config import get_config


tasks_router = APIRouter(prefix="/tasks")

app_config = get_config()


async def make_grpc_request(
    request_message,
    grpc_method,
):
    try:
        return await grpc_method(request_message)
    except RpcError as e:
        if e.code() == grpc.StatusCode.NOT_FOUND:
            raise HTTPException(status_code=404, detail="Task not found")


@tasks_router.post("/", response_model=TaskIdSchema)
async def create_task(task: TaskSchema, current_user: User = Depends(get_current_user), stub = Depends(get_stub)):
    create_task_request = tasks_pb2.CreateTaskRequest(
        title=task.title, 
        text=task.text, 
        author=current_user.username
    )
    return await stub.CreateTask(create_task_request)

@tasks_router.put("/{task_id}", response_model=FullTaskSchema)
async def update_task(
    task_id: UUID, 
    task: TaskSchema, 
    current_user: User = Depends(get_current_user),
    stub = Depends(get_stub)
):
    update_task_request = tasks_pb2.UpdateTaskRequest(
        task_id=str(task_id),
        title=task.title, 
        text=task.text,
        updater=current_user.username
    )
    return await make_grpc_request(update_task_request, stub.UpdateTask)

@tasks_router.delete("/{task_id}", response_model=DeleteTaskResponse)
async def delete_task(
    task_id: UUID, 
    current_user: User = Depends(get_current_user),
    stub = Depends(get_stub)
):
    delete_task_request = tasks_pb2.DeleteTaskRequest(
        task_id=str(task_id),
        user=current_user.username
    )
    return await make_grpc_request(delete_task_request, stub.DeleteTask)

@tasks_router.get("/{task_id}", response_model=FullTaskSchema)
async def get_task_by_id(
    task_id: UUID, 
    stub = Depends(get_stub),
    current_user: User = Depends(get_current_user),
):
    get_task_request = tasks_pb2.GetTaskByIdRequest(task_id=str(task_id))
    return await make_grpc_request(get_task_request, stub.GetTaskById)

@tasks_router.get("/all/", response_model=List[FullTaskSchema])
async def get_tasks(
    page_number: int = Query(gt=0),
    page_size: int = Query(gt=0),
    current_user: User = Depends(get_current_user),
    stub = Depends(get_stub)
):
    get_tasks_request = tasks_pb2.GetTasksRequest(
        page_number=page_number,
        page_size=page_size
    )
    return [response async for response in stub.GetTasks(get_tasks_request)]
