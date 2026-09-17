from uuid import UUID

from app.core.exceptions import ForbiddenException, NotFoundException
from sqlalchemy.orm import Session
from app.repositories import cart_repository, products_repository
from app.schemas.cart import CartInsert, CartUpdate


def get_cart(db: Session,user_id: int):
    cart = cart_repository.get_cart(db, user_id)

    if not cart:
       raise NotFoundException('Cart not found')

    return cart


def add_cart_item( cart_item: CartInsert, user_id: int, db: Session):
    product = products_repository.get_product_by_public_id(db, cart_item.product_id)

    if not product:
        raise NotFoundException('Product not found')
    
    current_cart = cart_repository.get_cart(db, user_id)
    existing_item = cart_repository.get_cart_item(db, current_cart.id, product.id)

    if existing_item:
        new_quantity = existing_item.quantity + cart_item.quantity
        item = cart_repository.update_cart_item(db, existing_item.id, new_quantity, product.price)
    else:
        cart_item_data = cart_item.model_dump()
        cart_item_data["cart_id"] = current_cart.id
        cart_item_data["product_id"] = product.id
        item = cart_repository.add_cart_item(db, cart_item_data, product.price)

    db.commit()
    db.refresh(item)
    return item



def update_cart_item(public_id: UUID, updated_data:CartUpdate, user_id:int, db: Session ):
    current_cart = cart_repository.get_cart(db, user_id)
    existing_item = cart_repository.get_cart_item_by_public_id(db, public_id)

    if not existing_item:
         raise NotFoundException('Product not found in Cart')
    
    if existing_item.cart_id != current_cart.id:
        raise ForbiddenException('Item does not belong to your cart')    
    
    product = products_repository.get_product_by_id(db, existing_item.product_id)
    updated_cart_item = cart_repository.update_cart_item(db, existing_item.id, updated_data.quantity, product.price)

    db.commit()
    db.refresh(updated_cart_item)
    return updated_cart_item


def delete_cart_item(public_id: UUID, user_id: int, db: Session):
    current_cart = cart_repository.get_cart(db, user_id)
    existing_item = cart_repository.get_cart_item_by_public_id(db, public_id)

    if not existing_item:
       raise NotFoundException('Product not found in Cart')
    
    if existing_item.cart_id != current_cart.id:
        raise ForbiddenException('Item does not belong to your cart')
    
    cart_repository.delete_cart_item_by_id(db, existing_item.id)
    db.commit()