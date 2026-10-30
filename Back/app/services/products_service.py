from uuid import UUID

from app.core.exceptions import ConflictException, NotFoundException
from sqlalchemy.orm import Session
from app.repositories import products_repository, cart_repository
from app.schemas.products import ProductCreate, ProductUpdate


def get_all_products(db: Session):
    products_list = products_repository.get_all_products(db)

    return products_list


def get_product(db: Session, public_id: UUID):
    product = products_repository.get_product_by_public_id(db,public_id)

    if not product:
       raise NotFoundException('Product not found')

    return product


def create_product(db: Session, product_data: ProductCreate):
    product = products_repository.create_new_product(db, product_data.model_dump())
    db.commit()
    db.refresh(product)
    return product


def update_product(db: Session, public_id: UUID, updated_data:ProductUpdate ):
    product = products_repository.get_product_by_public_id(db,public_id)

    if not product:
       raise NotFoundException('Product not found')

    updated_product = products_repository.update_product_by_id(db, product.id, updated_data.model_dump(exclude_unset=True))
    db.commit()
    db.refresh(updated_product)
    return updated_product


def delete_product(db: Session, public_id: UUID ):
    product = products_repository.get_product_by_public_id(db,public_id)

    if not product:
       raise NotFoundException('Product not found')

    if products_repository.product_has_orders(db, product.id):
        raise ConflictException('Product is part of existing orders and cannot be deleted')

    cart_repository.delete_cart_items_by_product(db, product.id)
    products_repository.delete_product_by_id(db, product.id)
    db.commit()

