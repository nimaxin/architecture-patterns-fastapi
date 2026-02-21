from typing import Protocol

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ..domain import Batch


class RepositoryProtocol(Protocol):
    async def add(self, batch: Batch) -> None: ...
    async def get(self, reference: str) -> Batch | None: ...
    async def list(self) -> list[Batch]: ...


class SQLAlchemyRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(self, batch: Batch) -> None:
        self.session.add(batch)
        await self.session.flush()

    async def get(self, reference: str) -> Batch | None:
        stmt = (
            select(Batch)
            .where(Batch.reference == reference)  # type: ignore
            .options(selectinload(Batch._allocations))  # type: ignore
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def list(self) -> list[Batch]:
        stmt = select(Batch).options(selectinload(Batch._allocations))  # type: ignore
        result = await self.session.execute(stmt)
        return list(result.scalars())


class FakeRepository:
    def __init__(self, batches: list[Batch]) -> None:
        self._batches = set(batches)

    async def add(self, batch: Batch) -> None:
        self._batches.add(batch)

    async def get(self, reference: str) -> Batch | None:
        return next(
            (batch for batch in self._batches if batch.reference == reference), None
        )

    async def list(self) -> list[Batch]:
        return list(self._batches)
