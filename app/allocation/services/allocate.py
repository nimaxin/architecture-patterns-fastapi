from sqlalchemy.ext.asyncio import AsyncSession

from app.allocation.adapters.repository import RepositoryProtocol

from .. import domain
from ..domain import OrderLine


async def allocate(
    sku: str,
    quantity: int,
    order_id: str,
    repository: RepositoryProtocol,
    session: AsyncSession,
) -> str:
    order_line = OrderLine(sku, quantity, order_id)
    batches = await repository.list()
    batch_ref = domain.allocate(order_line, batches)
    await session.commit()
    return batch_ref
