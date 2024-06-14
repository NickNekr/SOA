from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from contextlib import asynccontextmanager
from functools import lru_cache

from config import get_config
from database.model import Base  


@lru_cache
def get_engine() -> AsyncEngine:
    app_config = get_config()
    return create_async_engine(app_config.DataBase.SQLALCHEMY_DATABASE_URI, echo=True)

@lru_cache
def get_async_session():
    print("MYSESSION", get_engine().url)
    return sessionmaker(get_engine(), class_=AsyncSession, expire_on_commit=False)

@asynccontextmanager
async def get_session() -> AsyncSession: # type: ignore
    async with get_async_session()() as session:
        yield session
        await session.commit()



async def init_models():
    print("MYSESSION", get_engine().url)
    async with get_engine().begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)