import pytest

from app.allocation import usecases
from app.allocation.errors import OutOfStockError
from app.allocation.model import Batch, OrderLine
from app.allocation.repository import FakeRepository


class FakeSession:
    async def commit(self):
        pass


async def test_returns_allocation():
    order_line = OrderLine("chair", 1, "order-id")
    batch = Batch("batch-ref", "chair", 10)
    repository = FakeRepository([batch])
    session = FakeSession()

    batch_ref = await usecases.allocate(order_line, repository, session)  # type: ignore
    assert batch_ref == batch.reference


async def test_error_for_invalid_sku():
    order_line = OrderLine("unknown", 1, "order-id")
    batch = Batch("batch-ref", "chair", 10)
    repository = FakeRepository([batch])
    session = FakeSession()

    with pytest.raises(OutOfStockError):
        await usecases.allocate(order_line, repository, session)  # type: ignore
