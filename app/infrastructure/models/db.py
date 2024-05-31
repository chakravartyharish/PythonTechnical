from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from app.config import get_settings
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

DB_URL = "postgresql+asyncpg://user:password@db:5432/dbname"

engine = create_async_engine(DB_URL, echo=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session
