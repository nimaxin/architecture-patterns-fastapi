import pytest

from app.allocation import services
from app.allocation.adapters.repository import FakeRepository
from app.allocation.domain import Batch
from app.allocation.domain.errors import OutOfStockError


class FakeSession:
    async def commit(self):
        pass


async def test_returns_allocation():
    batch = Batch("batch-ref", "chair", 10)
    repository = FakeRepository([batch])
    session = FakeSession()

    batch_ref = await services.allocate("chair", 1, "order-id", repository, session)  # type: ignore
    assert batch_ref == batch.reference


async def test_error_for_invalid_sku():
    batch = Batch("batch-ref", "chair", 10)
    repository = FakeRepository([batch])
    session = FakeSession()

    with pytest.raises(OutOfStockError):
        await services.allocate("unknown", 1, "order-id", repository, session)  # type: ignore


async def test_add_batch():
    repository = FakeRepository([])
    await services.add_batch("batch-ref", "sku", 1, None, repository)
    assert await repository.get("batch-ref") is not None
