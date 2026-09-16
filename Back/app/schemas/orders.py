from decimal import Decimal
from typing import List

from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class ProductInOrderResponse(BaseModel):
    public_id: UUID
    name: str

    model_config = {"from_attributes": True}


class OrderItemResponse(BaseModel):
    product: ProductInOrderResponse
    quantity: int
    unit_price: Decimal

    model_config = {"from_attributes": True}


class OrderResponse(BaseModel):
    public_id: UUID
    status: str
    total:float
    created_at: datetime
    items: List[OrderItemResponse]

    model_config = {"from_attributes": True}
