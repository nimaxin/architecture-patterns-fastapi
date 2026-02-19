from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from .model import Batch


class SQLAlchemyRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(self, batch: Batch) -> Batch:
        self.session.add(batch)
        await self.session.flush()
        return batch

    async def get(self, reference: str) -> Batch | None:
        stmt = (
            select(Batch)
            .where(Batch.reference == reference)
            .options(selectinload(Batch._allocations))
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def list(self) -> list[Batch]:
        stmt = select(Batch)
        result = await self.session.execute(stmt)
        return list(result.scalars())
