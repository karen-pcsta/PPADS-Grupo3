from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel,Field
from typing import Optional

class ProductCreate(BaseModel):
    name:str
    description: Optional[str] = None
    price: Decimal = Field(gt=0, le=99999.99)

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[Decimal] = Field(default=None, gt=0, le=99999.99)

class ProductResponse(BaseModel):
    public_id: UUID
    name:str
    description: Optional[str] = None
    price:Decimal

    model_config = {"from_attributes": True}

