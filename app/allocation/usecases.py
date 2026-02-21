from sqlalchemy.ext.asyncio import AsyncSession

from . import services
from .model import OrderLine
from .protocol import RepositoryProtocol


async def allocate(
    order_line: OrderLine, repository: RepositoryProtocol, session: AsyncSession
) -> str:
    batches = await repository.list()
    batch_ref = services.allocate(order_line, batches)
    await session.commit()
    return batch_ref
