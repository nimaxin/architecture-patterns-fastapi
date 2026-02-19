from datetime import datetime

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    MappedAsDataclass,
    mapped_column,
    relationship,
)


class BaseModel(MappedAsDataclass, DeclarativeBase):
    pass


class OrderLine(BaseModel):
    __tablename__ = "order_line"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)

    sku: Mapped[str]
    quantity: Mapped[int]
    order_id: Mapped[str]

    batch_id: Mapped[int | None] = mapped_column(
        ForeignKey("batch.id", ondelete="SET NULL"), default=None
    )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, OrderLine):
            return False
        return self.order_id == other.order_id and self.sku == other.sku

    def __hash__(self) -> int:
        return hash((self.order_id, self.sku))


class Batch(BaseModel):
    __tablename__ = "batch"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)

    reference: Mapped[str]
    sku: Mapped[str]
    quantity: Mapped[int]
    eta: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)
    _allocations: Mapped[set[OrderLine]] = relationship(default_factory=set)

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
