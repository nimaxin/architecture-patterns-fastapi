from dataclasses import dataclass
from datetime import datetime

from .errors import OutOfStockError


@dataclass(unsafe_hash=True)
class OrderLine:
    sku: str
    quantity: int
    order_id: str


class Batch:
    def __init__(
        self, reference: str, sku: str, quantity: int, eta: datetime | None = None
    ):
        self.reference = reference
        self.sku = sku
        self.quantity = quantity
        self.eta = eta
        self._allocations: set[OrderLine] = set()

    @property
    def available_quantity(self) -> int:
        return self.quantity - sum(
            order_lines.quantity for order_lines in self._allocations
        )

    def allocate(self, order_line: OrderLine):
        self._allocations.add(order_line)

    def can_allocate(self, order_line: OrderLine) -> bool:
        return (
            self.sku == order_line.sku
            and self.available_quantity >= order_line.quantity
        )

    def deallocate(self, order_line: OrderLine):
        if order_line in self._allocations:
            self._allocations.remove(order_line)

    def __lt__(self, other: Batch):
        if self.eta is None:
            return True
        if other.eta is None:
            return False
        return self.eta < other.eta

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Batch):
            return False

        return self.reference == value.reference

    def __hash__(self) -> int:
        return hash(self.reference)


def allocate(order_line: OrderLine, batches: list[Batch]) -> str:
    try:
        batch = next(b for b in sorted(batches) if b.can_allocate(order_line))
        batch.allocate(order_line)
        return batch.reference
    except StopIteration:
        raise OutOfStockError()
