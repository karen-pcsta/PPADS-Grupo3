from typing import List
from uuid import UUID

from sqlalchemy.orm import Session
from app.models.models import CartItem, Order,OrderItem


def get_all_orders(db: Session, user_id: int = None):
    query = db.query(Order)
    if user_id:
        query = query.filter(Order.user_id == user_id)
    return query.all()

def get_order_by_public_id(db: Session, public_id: UUID):
    return db.query(Order).filter(Order.public_id == public_id).first()

def create_order_with_items(db: Session, user_id: int, total: float, items: list, cart_id: int):
    order = Order(user_id=user_id, total=total, status="pending")
    db.add(order)
    db.flush()
    
    db.add_all([
        OrderItem(
            order_id=order.id,
            product_id=item["product_id"],
            quantity=item["quantity"],
            unit_price=item["unit_price"],
        )
        for item in items
    ])
    
    db.query(CartItem).filter(CartItem.cart_id == cart_id).delete()
    db.flush()
    
    return order



