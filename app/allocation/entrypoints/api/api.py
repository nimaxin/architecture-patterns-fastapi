from fastapi import FastAPI, HTTPException

from app.allocation import services
from app.allocation.adapters.repository import SQLAlchemyRepository
from app.allocation.domain.errors import OutOfStockError

from .depends import get_session
from .schemas import AllocateRequest, AllocateResponse

api = FastAPI()


@api.post("/allocate", status_code=201)
async def allocate_order_line(data: AllocateRequest):
    async with get_session() as session:
        try:
            batch_ref = await services.allocate(
                sku=data.sku,
                quantity=data.quantity,
                order_id=data.order_id,
                repository=SQLAlchemyRepository(session),
                session=session,
            )
        except OutOfStockError:
            raise HTTPException(400, detail="out_of_stock")

    return AllocateResponse(batch_ref=batch_ref)
