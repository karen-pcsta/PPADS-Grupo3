from uuid import UUID

from sqlalchemy.orm import Session
from app.models.models import Product


def get_all_products(db: Session):
    return db.query(Product).all()

def get_product_by_public_id(db: Session, public_id: UUID):
    return db.query(Product).filter(Product.public_id == public_id).first()

def get_product_by_id(db: Session, id: int):
    return db.query(Product).filter(Product.id == id).first()

def create_new_product(db: Session, product_data: dict):
    product = Product(**product_data)
    db.add(product)
    db.flush()
    return product

def update_product_by_id(db: Session, id:int, updated_data: dict):
    product = db.query(Product).filter(Product.id == id).first()

    for field, value in updated_data.items():
        setattr(product, field, value)

    db.flush()
    return product

def delete_product_by_id(db: Session, id:int):
    product_to_delete = db.query(Product).filter(Product.id == id).first()
    db.delete(product_to_delete)
    db.flush()

