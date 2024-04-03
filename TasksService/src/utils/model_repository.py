from functools import lru_cache

from common.repository import BaseRepository
from common.schema import TaskSchema
from database.model import Task

@lru_cache
def get_task_repo():
    return BaseRepository(Task, TaskSchema)