from fastapi import FastAPI, HTTPException

from . import usecases
from .depends import get_session
from .errors import OutOfStockError
from .model import OrderLine
from .repository import SQLAlchemyRepository
from .schemas import AllocateRequest, AllocateResponse

api = FastAPI()


@api.post("/allocate", status_code=201)
async def allocate_order_line(data: AllocateRequest):
    async with get_session() as session:
        order_line = OrderLine(
            sku=data.sku, quantity=data.quantity, order_id=data.order_id
        )
        try:
            batch_ref = await usecases.allocate(
                order_line, SQLAlchemyRepository(session), session
            )
        except OutOfStockError:
            raise HTTPException(400, detail="out_of_stock")

    return AllocateResponse(batch_ref=batch_ref)
