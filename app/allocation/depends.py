from contextlib import asynccontextmanager
from typing import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import Session


@asynccontextmanager
async def get_session() -> AsyncIterator[AsyncSession]:
    async with Session() as session:
        async with session.begin():
            yield session
