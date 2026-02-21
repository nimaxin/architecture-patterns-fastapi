import pytest

from app.allocation import services
from app.allocation.adapters.repository import FakeRepository
from app.allocation.domain import Batch, OrderLine
from app.allocation.domain.errors import OutOfStockError


class FakeSession:
    async def commit(self):
        pass


async def test_returns_allocation():
    order_line = OrderLine("chair", 1, "order-id")
    batch = Batch("batch-ref", "chair", 10)
    repository = FakeRepository([batch])
    session = FakeSession()

    batch_ref = await services.allocate(order_line, repository, session)  # type: ignore
    assert batch_ref == batch.reference


async def test_error_for_invalid_sku():
    order_line = OrderLine("unknown", 1, "order-id")
    batch = Batch("batch-ref", "chair", 10)
    repository = FakeRepository([batch])
    session = FakeSession()

    with pytest.raises(OutOfStockError):
        await services.allocate(order_line, repository, session)  # type: ignore
