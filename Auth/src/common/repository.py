from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from functools import lru_cache

from common.schema import UserSchema
from database.model import User, UserData


class UserRepository:
    async def create_user(self, user: UserSchema, session: AsyncSession):
        empty_user_data = UserData()
        session.add(empty_user_data)
        await session.flush()
        await session.refresh(empty_user_data)

        new_user = User(
            username=user.username,
            hashed_password=user.password,
            user_data_id=empty_user_data.id
        )

        session.add(new_user)
        await session.flush()
        await session.refresh(new_user)

        await session.commit()

        return new_user.id

    async def get_user(self, username: str, session: AsyncSession) -> User:
        user = await session.execute(select(User).where(User.username == username))
        return user.scalar()

@lru_cache
def get_user_repo():
    return UserRepository()