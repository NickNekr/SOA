from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from config import get_config
from database.model import Base  

app_config = get_config()

engine: AsyncEngine = create_async_engine(app_config.DataBase.SQLALCHEMY_DATABASE_URI, echo=True, future=True)

async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False, future=True)

async def get_session() -> AsyncSession: # type: ignore
    async with async_session() as session:
        yield session
        await session.commit()


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)