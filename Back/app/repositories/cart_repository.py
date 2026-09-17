from uuid import UUID

from sqlalchemy.orm import Session
from app.models.models import Cart,CartItem


def get_cart(db: Session, user_id:id):
    return db.query(Cart).filter(Cart.user_id == user_id).first()

def get_cart_item(db: Session, cart_id:id, product_id:id):
    return db.query(CartItem).filter(
        CartItem.cart_id == cart_id,
        CartItem.product_id == product_id).first()


def update_cart_item( db: Session, existing_item_id:int, quantity:int, price:float):
    existing_item = db.query(CartItem).filter(CartItem.id == existing_item_id).first()

    existing_item.quantity = quantity
    existing_item.unit_price = price

    db.flush()
    return existing_item
    

def add_cart_item(db: Session, cart_item_data: dict , price:float):
    cart_item = CartItem(**cart_item_data)
    cart_item.unit_price = price

    db.add(cart_item)
    db.flush()
    return cart_item


def get_cart_item_by_id(db: Session, id:int):
     return db.query(CartItem).filter(CartItem.id == id).first()

def get_cart_item_by_public_id(db: Session, public_id: UUID):
    return db.query(CartItem).filter(CartItem.public_id == public_id).first()


def delete_cart_item_by_id(db: Session, id:int):
    item_to_delete = db.query(CartItem).filter(CartItem.id == id).first()
    db.delete(item_to_delete)
    db.flush()

def delete_all_cart_items(db: Session, cart_id: int):
    db.query(CartItem).filter(CartItem.cart_id == cart_id).delete()
    db.flush()



