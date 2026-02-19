from typing import AsyncGenerator

import pytest
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession

from app.allocation.model import BaseModel

load_dotenv(dotenv_path=".env.test")


@pytest.fixture()
async def session() -> AsyncGenerator[AsyncSession, None]:
    from app.database.session import Session, engine

    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)

    async with engine.connect() as conn:
        async with Session(bind=conn, expire_on_commit=False) as session:
            yield session
