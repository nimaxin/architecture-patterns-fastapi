from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.allocation.model import Batch, OrderLine
from app.allocation.repository import SQLAlchemyRepository


async def test_repository_can_save_a_batch(session: AsyncSession):
    batch = Batch("batch-id", "chair", 15, datetime(2026, 1, 1))

    repository = SQLAlchemyRepository(session)
    await repository.add(batch)

    stmt = select(Batch)
    result = await session.execute(stmt)

    assert batch == result.scalar_one_or_none()


async def test_repository_can_retrieve_a_batch_with_allocations(session: AsyncSession):
    order_line = OrderLine("chair", 1, "order-1")
    batch = Batch("batch-id", "chair", 10)

    session.add(order_line)
    session.add(batch)
    await session.flush()

    batch.allocate(order_line)
    await session.flush()

    repository = SQLAlchemyRepository(session)
    db_batch = await repository.get(batch.reference)

    assert db_batch
    assert db_batch == batch
    assert db_batch.sku == batch.sku
    assert db_batch._allocations == {order_line}
    assert db_batch.available_quantity == batch.available_quantity
