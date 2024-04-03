import grpc
from sqlalchemy import select


from common.proto import tasks_pb2_grpc
from common.proto import tasks_pb2

from database.session import get_session
from database.model import Task

from config import get_config

from utils.model_repository import get_task_repo

task_repo = get_task_repo()

def task_exist(task, context):
    if task:
        return True
    context.set_code(grpc.StatusCode.NOT_FOUND)
    context.set_details("Task not found")
    return False


class TaskService(tasks_pb2_grpc.TaskServiceServicer):
    def __init__(self):
        pass

    async def CreateTask(self, request, context):
        async with get_session() as session:
            new_task = Task(title=request.title, text=request.text, author=request.author)
            await task_repo.add_model_instance(new_task, session)
            return tasks_pb2.Task(task_id=str(new_task.id), title=request.title, text=request.text, author=request.author)

    async def UpdateTask(self, request, context):
        async with get_session() as session:
            task = await task_repo.get_by_condition((Task.id == request.task_id) & (Task.author == request.updater), session)
            if not task_exist(task, context):
                return
            task.title = request.title
            task.text = request.text
            await session.commit()
            return tasks_pb2.Task(task_id=request.task_id, title=request.title, text=request.text)

    async def DeleteTask(self, request, context):
        async with get_session() as session:
            task = await task_repo.get_by_condition((Task.id == request.task_id) & (Task.author == request.user), session)
            if not task_exist(task, context):
                return
            await task_repo.delete_obj(task, session)
            return tasks_pb2.DeleteTaskResponse(success=True)

    async def GetTaskById(self, request, context):
        async with get_session() as session:
            task = await task_repo.get_by_condition((Task.id == request.task_id) & (Task.author == request.user), session)
            if not task_exist(task, context):
                return
            return tasks_pb2.Task(task_id=str(task.id), title=task.title, text=task.text)

    async def GetTasks(self, request, context):
        async with get_session() as session:
            offset = (request.page_number - 1) * request.page_size
            tasks = await session.execute(select(Task).where(Task.author == request.user).offset(offset).limit(request.page_size))
            tasks = tasks.scalars()
            
            if tasks:
                tasks = tasks.all()
                for task in tasks:
                    yield tasks_pb2.Task(task_id=str(task.id), title=task.title, text=task.text)
            

async def serve():
    config = get_config()
    server = grpc.aio.server()
    tasks_pb2_grpc.add_TaskServiceServicer_to_server(TaskService(), server)
    server.add_insecure_port(f'[::]:{config.Grpc.PORT}')
    await server.start()
    print("Server started!")
    await server.wait_for_termination()
