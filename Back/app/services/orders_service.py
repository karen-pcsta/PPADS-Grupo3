from uuid import UUID

from app.core.exceptions import BadRequestException, ForbiddenException, NotFoundException
from sqlalchemy.orm import Session
from app.repositories import orders_repository,cart_repository


def create_order(db: Session, user_id:int):
    cart = cart_repository.get_cart(db, user_id)

    if not cart or not cart.items:
        raise BadRequestException('Empty cart')
    
    total = sum(item.quantity * item.unit_price for item in cart.items)
    items = [{"product_id": i.product_id, "quantity": i.quantity, "unit_price": i.unit_price} for i in cart.items]

    order = orders_repository.create_order_with_items(db, user_id, total, items, cart.id)
    db.commit()
    db.refresh(order)
    return order


def get_all_orders(db: Session, user_id: int, user_role: str):
    if user_role == "admin":
        return orders_repository.get_all_orders(db)
    return orders_repository.get_all_orders(db, user_id)

def get_order_by_public_id(db: Session, public_id: UUID, user_id:int, user_role: str):
    order = orders_repository.get_order_by_public_id(db,public_id)

    if not order:
       raise NotFoundException('Order not found')

    if user_role != "admin" and order.user_id != user_id:
        raise ForbiddenException('Not Authorized')

    return order


