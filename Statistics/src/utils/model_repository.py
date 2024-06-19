from functools import lru_cache

from common.repository import BaseRepository
from common.schema import LikesStatsSchema, ViewsStatsSchema, TaskToAuthorSchema
from Statistics.src.database.model import ViewsStats, LikesStats, TaskToAuthor

@lru_cache
def get_likes_repo():
    return BaseRepository(LikesStats, LikesStatsSchema)

@lru_cache
def get_views_repo():
    return BaseRepository(ViewsStats, ViewsStatsSchema)

@lru_cache
def get_task_to_author_repo():
    return BaseRepository(TaskToAuthor, TaskToAuthorSchema)
