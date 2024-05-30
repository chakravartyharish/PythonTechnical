from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from app.config import get_settings

from sqlalchemy.orm import sessionmaker

Base = declarative_base()

# Create the engine using the databaseURL from settings
engine = create_async_engine(str(get_settings().db_url), echo=True)
# Create async session maker
async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session
