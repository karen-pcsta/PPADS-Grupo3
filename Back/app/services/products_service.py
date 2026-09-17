from uuid import UUID

from app.core.exceptions import NotFoundException
from sqlalchemy.orm import Session
from app.repositories import products_repository


def get_all_products(db: Session):
    products_list = products_repository.get_all_products(db)

    return products_list


def get_product(db: Session, public_id: UUID):
    product = products_repository.get_product_by_public_id(db,public_id)

    if not product:
       raise NotFoundException('Product not found')

    return product

