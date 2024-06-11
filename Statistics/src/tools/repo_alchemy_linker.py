from functools import lru_cache
import pickle

from database.model import Views, Likes, LikesStats, ViewsStats
from database.session import get_session_outside_depends
from common.repository import BaseRepository
from common.schema import ViewsSchema, LikesSchema, LikesStatsSchema, ViewsStatsSchema

class MonoRepos:
    def __init__(self) -> None:
        self.views = BaseRepository(Views, ViewsSchema)
        self.likes = BaseRepository(Likes, LikesSchema)
        self.likes_stats = BaseRepository(LikesStats, LikesStatsSchema)
        self.views_stats = BaseRepository(ViewsStats, ViewsStatsSchema)
    
    def get_state(self, entity):
        return (self.views, self.views_stats, ViewsStats) if entity == Views else (self.likes, self.likes_stats, LikesStats)
    
    async def ProduceEntity(self, msg, entity):
        data = pickle.loads(msg.value)
        repo, stats_repo, stats_entity = self.get_state(entity)

        async with get_session_outside_depends() as session:
            async with session.begin():
                obj = await repo.get_by_condition((entity.task_id == data["task_id"]) & (entity.username == data["username"]), session)
                if obj is not None:
                    return

                await repo.add_model_instance(entity(task_id=data["task_id"], username=data["username"]), session)
                obj_stats = await stats_repo.get_by_condition((stats_entity.task_id == data["task_id"]), session)
                if obj_stats is None:
                    obj_stats = stats_entity(task_id=data["task_id"])
                    await stats_repo.add_model_instance(obj_stats, session)

                obj_stats.count += 1
                await session.flush()

@lru_cache
def get_mono_repos():
    return MonoRepos()