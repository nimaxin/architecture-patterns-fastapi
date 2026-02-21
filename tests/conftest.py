from typing import Any, AsyncGenerator

import pytest
from dotenv import load_dotenv
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.allocation.adapters.orm import metadata, start_mappers
from app.allocation.domain import Batch

load_dotenv(dotenv_path=".env.test")
start_mappers()


@pytest.fixture()
async def session() -> AsyncGenerator[AsyncSession, None]:
    from app.database.session import Session, engine

    async with engine.begin() as conn:
        await conn.run_sync(metadata.drop_all)
        await conn.run_sync(metadata.create_all)

    async with engine.connect() as conn:
        async with Session(bind=conn, expire_on_commit=False) as session:
            yield session


@pytest.fixture()
def add_batch(session: AsyncSession):
    async def _add_batch(batches: list[dict[str, Any]]):
        stmt = insert(Batch).values(batches)
        await session.execute(stmt)
        await session.commit()

    yield _add_batch
