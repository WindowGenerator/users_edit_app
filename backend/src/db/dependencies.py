from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession


# Dependency
async def get_session(request: Request) -> AsyncSession:
    async_session =  request.app.state.db
    async with async_session() as session:
        yield session