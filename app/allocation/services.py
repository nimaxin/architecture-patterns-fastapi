from .errors import OutOfStockError
from .model import Batch, OrderLine


def allocate(order_line: OrderLine, batches: list[Batch]) -> str:
    try:
        batch = next(b for b in sorted(batches) if b.can_allocate(order_line))
        batch.allocate(order_line)
        return batch.reference
    except StopIteration:
        raise OutOfStockError()
