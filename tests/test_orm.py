from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.allocation.model import OrderLine
from app.allocation.orm import start_mappers


async def test_order_line_mapper_can_load_order_lines(session: AsyncSession):
    start_mappers()

    order_lines = [
        {"sku": "chair", "quantity": 10, "order_id": "order-1"},
        {"sku": "table", "quantity": 2, "order_id": "order-2"},
    ]
    stmt = insert(OrderLine).values(order_lines)
    await session.execute(stmt)

    stmt = select(OrderLine)
    result = await session.execute(stmt)

    assert result.scalars().all() == [
        OrderLine(**order_line) for order_line in order_lines
    ]
