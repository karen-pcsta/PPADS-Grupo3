from uuid import UUID

from pydantic import BaseModel,Field
from typing import List, Optional
from decimal import Decimal



class ProductInCartResponse(BaseModel):
    public_id: UUID
    name: str

    model_config = {"from_attributes": True}

class CartItemResponse(BaseModel):
    public_id: UUID
    product: ProductInCartResponse
    quantity:int
    unit_price: Decimal

    model_config = {"from_attributes": True}

class CartResponse(BaseModel):
    public_id: UUID
    items: List[CartItemResponse]

    model_config = {"from_attributes": True} 


class CartInsert(BaseModel):
    product_id: UUID
    quantity:int = Field(gt=0)

class CartUpdate(BaseModel):
    quantity:int = Field(gt=0)

