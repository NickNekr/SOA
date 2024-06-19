from functools import lru_cache

from common.repository import BaseRepository
from common.schema import UserSchema, UserDataSchema
from Auth.src.database.model import User, UserData

@lru_cache
def get_user_repo():
    return BaseRepository(User, UserSchema)

@lru_cache
def get_user_data_repo():
    return BaseRepository(UserData, UserDataSchema)