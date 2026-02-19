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
    Column("order_id", String, nullable=False),
    Column(
        "batch_id",
        Integer,
        ForeignKey("batch.id", ondelete="SET NULL"),
        nullable=True,
    ),
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


def start_mappers():
    mapper_registry.map_imperatively(OrderLine, order_line)
    mapper_registry.map_imperatively(
        Batch,
        batch,
        properties={"_allocations": relationship(OrderLine, collection_class=set)},
    )
