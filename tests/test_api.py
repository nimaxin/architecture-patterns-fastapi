import uuid
from datetime import datetime

from httpx import ASGITransport, AsyncClient

from app.allocation.api import api

client = AsyncClient(transport=ASGITransport(api), base_url="http://test")


def random_ref() -> str:
    return uuid.uuid4().hex


async def test_happy_path_returns_201_and_allocated_batch(add_batch):
    sku = "chair"
    later_datetime = datetime(2025, 1, 2)
    early_datetime = datetime(2025, 1, 1)
    batches = [
        {
            "reference": random_ref(),
            "sku": sku,
            "quantity": 100,
            "eta": later_datetime,
        },
        {
            "reference": random_ref(),
            "sku": sku,
            "quantity": 100,
            "eta": early_datetime,
        },
        {
            "reference": random_ref(),
            "sku": "table",
            "quantity": 100,
            "eta": None,
        },
    ]
    await add_batch(batches)
    data = {"order_id": random_ref(), "sku": "chair", "quantity": 3}
    response = await client.post("/allocate", json=data)
    assert response.status_code == 201
    assert response.json()["batch_ref"] == batches[1]["reference"]


async def test_unhappy_path_returns_400_and_error_message():
    data = {"order_id": random_ref(), "sku": "unknown-sku", "quantity": 3}
    response = await client.post("/allocate", json=data)
    assert response.status_code == 400
