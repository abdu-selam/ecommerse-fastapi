from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.utils.env import settings
from sqlalchemy.orm import DeclarativeBase

engine = create_async_engine(settings.PG_KEY)
SessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)

class Base(DeclarativeBase):
    ...

async def create_tables():
    async with engine.begin() as con:
        await con.run_sync(Base.metadata.create_all)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as db:
        yield db
