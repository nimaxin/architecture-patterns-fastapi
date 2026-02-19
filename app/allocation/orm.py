from sqlalchemy import Column, DateTime, ForeignKey, Integer, MetaData, String, Table
from sqlalchemy.orm import registry, relationship

from .model import Batch, OrderLine

mapper_registry = registry()
metadata = MetaData()

order_line = Table(
    "order_line",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("sku", String),
    Column("quantity", Integer, nullable=False),
    Column("order_id", Integer),
)

batch = Table(
    "batch",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("reference", String, nullable=False, unique=True),
    Column("sku", String, nullable=False),
    Column("quantity", Integer, nullable=False),
    Column("eta", DateTime(timezone=True), nullable=True),
)

batch_allocation = Table(
    "batch_allocation",
    metadata,
    Column(
        "batch_id",
        Integer,
        ForeignKey("batch.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "order_line_id",
        Integer,
        ForeignKey("order_line.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


def start_mappers():
    mapper_registry.map_imperatively(OrderLine, order_line)
    mapper_registry.map_imperatively(
        Batch,
        batch,
        properties={
            "_allocations": relationship(
                OrderLine,
                secondary=batch_allocation,
                collection_class=set,
            )
        },
    )
