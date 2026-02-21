from pydantic import BaseModel as BaseSchema
from pydantic import Field


class AllocateRequest(BaseSchema):
    sku: str = Field(
        ...,
        description="Unique product identifier (SKU) for the item being ordered.",
    )
    quantity: int = Field(
        ..., description="Quantity of the product to order. Must be a positive integer."
    )
    order_id: str = Field(
        ..., description="Unique identifier of the order that this item belongs to."
    )


class AllocateResponse(BaseSchema):
    batch_ref: str = Field(
        ..., description="Reference of the batch that the order line was allocated to."
    )
