from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.cart import CartInsert, CartUpdate,CartItemResponse,CartResponse
from app.services import cart_service
from app.core.dependencies import get_db, verify_jwt

router = APIRouter(prefix="/cart", tags=["cart"])

@router.get("/", response_model = CartResponse, status_code=200)
def get_cart(current_user = Depends(verify_jwt), db: Session = Depends(get_db)):
    return cart_service.get_cart(db, current_user.id)


@router.post("/items", response_model = CartItemResponse, status_code=201)
def add_cart_item( cart_item: CartInsert,current_user = Depends(verify_jwt), db: Session = Depends(get_db)):
    return cart_service.add_cart_item( cart_item, current_user.id, db)


@router.put("/items/{public_id}", response_model = CartItemResponse, status_code=200)
def update_cart_item(public_id: UUID,  updated_data:CartUpdate, current_user = Depends(verify_jwt), db: Session = Depends(get_db)):
    return cart_service.update_cart_item(public_id, updated_data, current_user.id, db)

@router.delete("/items/{public_id}", status_code=200)
def delete_cart_item(public_id: UUID, current_user = Depends(verify_jwt), db: Session = Depends(get_db)):
    return cart_service.delete_cart_item(public_id,current_user.id, db)