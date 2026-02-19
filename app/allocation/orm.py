from sqlalchemy import Column, Integer, MetaData, String, Table
from sqlalchemy.orm import registry

from .model import OrderLine

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


def start_mappers():
    mapper_registry.map_imperatively(OrderLine, order_line)
