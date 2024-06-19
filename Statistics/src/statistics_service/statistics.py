import grpc
from sqlalchemy import select, func

from common.statistics_proto import statistics_pb2_grpc
from common.statistics_proto import statistics_pb2
from Statistics.src.database.session import get_session_outside_depends
from Statistics.src.database.model import ViewsStats, LikesStats, TaskToAuthor
from Statistics.src.config import get_config
from Statistics.src.utils.model_repository import get_likes_repo, get_views_repo, get_task_to_author_repo

likes_repo = get_likes_repo()
views_repo = get_views_repo()
task_to_author_repo = get_task_to_author_repo()

def author_exist(task, context):
    if task:
        return True
    context.set_code(grpc.StatusCode.NOT_FOUND)
    context.set_details("Author not found")
    return False


class StatisticsService(statistics_pb2_grpc.StatisticsServiceServicer):
    def __init__(self):
        pass

    async def GetTaskStats(self, request, context):
        async with get_session_outside_depends() as session:
            views_statistics = await views_repo.get_by_condition(ViewsStats.task_id == request.task_id, session)
            likes_statistics = await likes_repo.get_by_condition(LikesStats.task_id == request.task_id, session)

            likes_count = 0 if not likes_statistics else likes_statistics.count
            views_count = 0 if not views_statistics else views_statistics.count

            return statistics_pb2.TaskStatsResponse(task_id=request.task_id, views=views_count, likes=likes_count)

    async def GetTopTasks(self, request, context):
        async with get_session_outside_depends() as session:
            entity = ViewsStats if request.sort_by == "views" else LikesStats

            stmt = (
                select(
                    entity.task_id,
                    entity.count,
                    TaskToAuthor.author
                )
                .join(TaskToAuthor, TaskToAuthor.task_id == entity.task_id)
                .order_by(entity.count.desc())
                .limit(5)
            )

            result = await session.execute(stmt)
            top_tasks = result.all()

            top_task_response = [
                statistics_pb2.Task(
                    task_id=str(task.task_id), 
                    author=task.author, 
                    count=task.count
                )
                for task in top_tasks
            ]

            return statistics_pb2.TopTasksResponse(task=top_task_response)

    async def GetTopUsers(self, request, context):
        async with get_session_outside_depends() as session:
            stmt = (
                select(
                    TaskToAuthor.author,
                    func.sum(LikesStats.count).label('total_likes')
                )
                .join(LikesStats, TaskToAuthor.task_id == LikesStats.task_id)
                .group_by(TaskToAuthor.author)
                .order_by(func.sum(LikesStats.count).desc())
                .limit(3)
            )

            result = await session.execute(stmt)
            top_users = result.all()

            top_users_response = [
                statistics_pb2.User(
                    login=user.author,
                    total_likes=user.total_likes
                )
                for user in top_users
            ]

            return statistics_pb2.TopUsersResponse(user=top_users_response)




async def server():
    config = get_config()
    server = grpc.aio.server()
    statistics_pb2_grpc.add_StatisticsServiceServicer_to_server(StatisticsService(), server)
    server.add_insecure_port(f'[::]:{config.Grpc.PORT}')
    await server.start()
    print("Server started!")
    await server.wait_for_termination()
