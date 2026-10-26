from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.products import ProductCreate, ProductUpdate, ProductResponse
from app.services import products_service
from app.core.dependencies import get_db, verify_admin, verify_jwt
from typing import List

router = APIRouter(prefix="/products", tags=["products"])

@router.get("/", response_model = List[ProductResponse], status_code=200)
def get_all_products(db: Session = Depends(get_db),current_user = Depends(verify_jwt)):
    return products_service.get_all_products(db)


@router.get("/{public_id}", response_model=ProductResponse, status_code=200)
def get_product(public_id: UUID, db: Session = Depends(get_db), current_user = Depends(verify_jwt)):
    return products_service.get_product(db, public_id)


@router.post("/", response_model = ProductResponse, status_code=201)
def create_product(product_data: ProductCreate, db: Session = Depends(get_db), current_user = Depends(verify_admin)):
    return products_service.create_product(db,product_data)


@router.put("/{public_id}", response_model=ProductResponse, status_code=200)
def update_product(public_id: UUID, updated_data: ProductUpdate, db: Session = Depends(get_db), current_user = Depends(verify_admin)):
    return products_service.update_product(db, public_id, updated_data)


@router.delete("/{public_id}", status_code=200)
def delete_product(public_id: UUID, db: Session = Depends(get_db), current_user = Depends(verify_admin)):
    return products_service.delete_product(db, public_id)

