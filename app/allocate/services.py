from .errors import OutOfStockError
from .model import Batch, OrderLine


def allocate(order_line: OrderLine, batches: list[Batch]) -> int:
    try:
        batch = next(b for b in sorted(batches) if b.can_allocate(order_line))
        batch.allocate(order_line)
        return batch.id
    except StopIteration:
        raise OutOfStockError()
