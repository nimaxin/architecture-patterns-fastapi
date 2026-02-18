from dataclasses import dataclass

import pytest


@dataclass(frozen=True)
class OrderLine:
    sku: str
    quantity: int


class Order:
    def __init__(self, id: int, lines: list[OrderLine]):
        self.id = id
        self.lines = lines


class Batch:
    def __init__(self, id: int, sku: str, quantity):
        self.id = id
        self.sku = sku
        self.quantity = quantity
        self._allocated_order_lines: set[OrderLine] = set()

    def allocate(self, order_line: OrderLine):
        self._allocated_order_lines.add(order_line)

    @property
    def available_quantity(self) -> int:
        return self.quantity - sum(
            order_lines.quantity for order_lines in self._allocated_order_lines
        )


def test_allocating_to_a_batch_reduces_the_available_quantity():
    batch = Batch(1, "chair", 10)
    order_line = OrderLine("chair", 5)
    batch.allocate(order_line)
    assert batch.available_quantity == 5


def test_can_allocate_if_available_greater_than_required():
    pytest.fail()


def test_cannot_allocate_if_available_smaller_than_required():
    pytest.fail()


def test_can_allocate_if_available_equal_to_required():
    pytest.fail()


def test_cannot_allocate_if_skus_do_not_match():
    pytest.fail()


def test_can_only_deallocate_allocated_lines():
    pytest.fail()


def test_allocation_is_idempotent():
    pytest.fail()


def test_prefers_current_stock_batches_to_shipments():
    pytest.fail()


def test_prefers_earlier_batches():
    pytest.fail()


def test_returns_allocated_batch_ref():
    pytest.fail()


def test_raises_out_of_stock_exception_if_cannot_allocate():
    pytest.fail()
