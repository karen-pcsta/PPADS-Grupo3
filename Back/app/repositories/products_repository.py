from uuid import UUID

from sqlalchemy.orm import Session
from app.models.models import Product


def get_all_products(db: Session):
    return db.query(Product).all()

def get_product_by_public_id(db: Session, public_id: UUID):
    return db.query(Product).filter(Product.public_id == public_id).first()

def get_product_by_id(db: Session, id: int):
    return db.query(Product).filter(Product.id == id).first()
