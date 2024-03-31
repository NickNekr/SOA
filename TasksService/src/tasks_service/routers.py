import grpc
from sqlalchemy import select


from grpc_tasks import tasks_pb2
from grpc_tasks import tasks_pb2_grpc
from config import get_config
from database.session import get_session
from database.model import Task

class TaskService(tasks_pb2_grpc.TaskServiceServicer):
    def __init__(self):
        pass

    async def CreateTask(self, request, context):
        async for session in get_session():
            new_task = Task(title=request.title, text=request.text, author=request.author)
            session.add(new_task)
            await session.commit()
            return tasks_pb2.Task(task_id=str(new_task.id), title=request.title, text=request.text, author=request.author)

    async def UpdateTask(self, request, context):
        async for session in get_session():
            task = await session.get(Task, request.task_id)
            task.title = request.title
            task.text = request.text
            await session.commit()
            return tasks_pb2.Task(task_id=request.task_id, title=request.title, text=request.text)

    async def DeleteTask(self, request, context):
        async for session in get_session():
            task = await session.get(Task, request.task_id)
            session.delete(task)
            await session.commit()
            return tasks_pb2.DeleteTaskResponse(success=True)

    async def GetTaskById(self, request, context):
        async for session in get_session():
            task = await session.get(Task, request.task_id)
            return tasks_pb2.Task(task_id=str(task.id), title=task.title, text=task.text)

    async def GetTasks(self, request, context):
        async for session in get_session():
            tasks = await session.execute(select(Task))
            tasks = tasks.scalars().all()
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
