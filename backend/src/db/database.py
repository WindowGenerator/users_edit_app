from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncEngine
from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


async def async_session(asyncpg_url: str) -> AsyncEngine:
    engine = create_async_engine(asyncpg_url, echo=True)
    _async_session = sessionmaker(
        engine, expire_on_commit=False, autocommit=False, autoflush=False, class_=AsyncSession
    )
    return _async_session
