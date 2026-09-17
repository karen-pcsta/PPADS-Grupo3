from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.orders import OrderResponse
from app.services import orders_service
from app.core.dependencies import get_db, verify_jwt
from typing import List

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("/", response_model = OrderResponse, status_code=201)
def create_order(current_user = Depends(verify_jwt), db: Session = Depends(get_db)):
    return orders_service.create_order(db,current_user.id)


@router.get("/", response_model = List[OrderResponse], status_code=200)
def get_all_orders(current_user = Depends(verify_jwt),db: Session = Depends(get_db)):
    return orders_service.get_all_orders(db, current_user.id, current_user.role)


@router.get("/{public_id}", response_model = OrderResponse, status_code=200)
def get_order(public_id: UUID, current_user = Depends(verify_jwt), db: Session = Depends(get_db)):
    return orders_service.get_order_by_public_id(db, public_id, current_user.id, current_user.role)

