from datetime import datetime

from ..adapters.repository import RepositoryProtocol
from ..domain import Batch


async def add_batch(
    reference: str,
    sku: str,
    quantity: int,
    eta: datetime | None,
    repository: RepositoryProtocol,
):
    batch = Batch(reference, sku, quantity, eta)
    await repository.add(batch)
