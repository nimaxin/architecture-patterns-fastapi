from sqlalchemy.ext.asyncio import AsyncSession

from app.allocation.adapters.repository import RepositoryProtocol

from .. import domain
from ..domain import OrderLine


async def allocate(
    order_line: OrderLine, repository: RepositoryProtocol, session: AsyncSession
) -> str:
    batches = await repository.list()
    batch_ref = domain.allocate(order_line, batches)
    await session.commit()
    return batch_ref
