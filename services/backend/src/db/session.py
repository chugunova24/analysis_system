# Standard Library imports
from typing import AsyncGenerator

# Core FastAPI imports

# Third-party imports
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# App imports
from src.config import settings


engine = create_async_engine(settings.PG_DATABASE_URL, echo=True)
async_session_maker = sessionmaker(bind=engine,
                                   class_=AsyncSession,
                                   expire_on_commit=False,
                                   # autoflush=True,
                                   )

sync_engine = create_engine(settings.PG_SYNC_DATABASE_URL, echo=True)
sync_session_maker = sessionmaker(
    autocommit=False,
    # autoflush=True,
    bind=sync_engine,
)


# билдер асинхронной сессии
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
