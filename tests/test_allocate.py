from datetime import datetime

import pytest

from app.allocate.errors import OutOfStockError
from app.allocate.model import Batch, OrderLine
from app.allocate.services import allocate


def test_allocating_to_a_batch_reduces_the_available_quantity():
    batch = Batch(1, "chair", 10)
    order_line = OrderLine("chair", 5)
    batch.allocate(order_line)
    assert batch.available_quantity == 5


def test_can_allocate_if_available_greater_than_required():
    batch = Batch(1, "chair", 10)
    order_line = OrderLine("chair", 5)
    assert batch.can_allocate(order_line)


def test_cannot_allocate_if_available_smaller_than_required():
    batch = Batch(1, "chair", 5)
    order_line = OrderLine("chair", 10)
    assert batch.can_allocate(order_line) is False


def test_can_allocate_if_available_equal_to_required():
    batch = Batch(1, "chair", 10)
    order_line = OrderLine("chair", 10)
    assert batch.can_allocate(order_line)


def test_cannot_allocate_if_skus_do_not_match():
    batch = Batch(1, "chair", 10)
    order_line = OrderLine("table", 1)
    assert batch.can_allocate(order_line) is False


def test_can_only_deallocate_allocated_lines():
    batch = Batch(1, "chair", 10)
    order_line = OrderLine("chair", 1)
    batch.deallocate(order_line)
    assert batch.available_quantity == 10


def test_allocation_is_idempotent():
    batch = Batch(1, "chair", 10)
    order_line = OrderLine("chair", 1)
    batch.allocate(order_line)
    batch.allocate(order_line)
    assert batch.available_quantity == 9


def test_prefers_current_stock_batches_to_shipments():
    shipment_batch = Batch(1, "chair", 10, datetime(2026, 1, 1))
    in_stock_batch = Batch(2, "chair", 10)
    order_line = OrderLine("chair", 1)
    allocate(order_line, [shipment_batch, in_stock_batch])
    assert shipment_batch.quantity == 10
    assert in_stock_batch.available_quantity == 9


def test_prefers_earlier_batches():
    earliest = Batch(1, "chair", 10, datetime(2026, 1, 1))
    medium = Batch(2, "chair", 10, datetime(2026, 1, 2))
    latest = Batch(3, "chair", 10, datetime(2026, 1, 3))
    order_line = OrderLine("chair", 1)
    allocate(order_line, [latest, medium, earliest])
    assert earliest.available_quantity == 9
    assert medium.available_quantity == 10
    assert latest.available_quantity == 10


def test_returns_allocated_batch_id():
    batches = [Batch(1, "chair", 10, datetime(2026, 1, 2))]
    order_line = OrderLine("chair", 1)
    batch_id = allocate(order_line, batches)
    assert batch_id == 1


def test_raises_out_of_stock_exception_if_cannot_allocate():
    batches = [
        Batch(1, "chair", 10, datetime(2026, 1, 2)),
        Batch(1, "table", 10, datetime(2026, 1, 2)),
    ]
    order_line = OrderLine("spoon", 1)
    with pytest.raises(OutOfStockError):
        allocate(order_line, batches)
