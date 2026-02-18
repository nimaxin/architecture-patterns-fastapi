from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class OrderLine:
    sku: str
    quantity: int


class Batch:
    def __init__(self, id: int, sku: str, quantity: int, eta: datetime | None = None):
        self.id = id
        self.sku = sku
        self.quantity = quantity
        self.eta = eta
        self._allocated_order_lines: set[OrderLine] = set()

    @property
    def available_quantity(self) -> int:
        return self.quantity - sum(
            order_lines.quantity for order_lines in self._allocated_order_lines
        )

    def allocate(self, order_line: OrderLine):
        self._allocated_order_lines.add(order_line)

    def can_allocate(self, order_line: OrderLine) -> bool:
        return (
            self.sku == order_line.sku
            and self.available_quantity >= order_line.quantity
        )

    def deallocate(self, order_line: OrderLine):
        if order_line in self._allocated_order_lines:
            self._allocated_order_lines.remove(order_line)

    def __lt__(self, other: Batch):
        if self.eta is None:
            return True
        if other.eta is None:
            return False
        return self.eta < other.eta
