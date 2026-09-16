from sqlalchemy.orm import Session
from app.models.models import User, Cart

def get_by_username(db: Session, username:str):
    return db.query(User).filter(User.username == username).first()

def get_by_public_id(db: Session, public_id: str):
    return db.query(User).filter(User.public_id == public_id).first()

def get_by_email(db: Session, email:str):
    return db.query(User).filter(User.email == email).first()


def create_new_user(db: Session, user_data: dict):
    user = User(**user_data)
    db.add(user)
    db.flush() 
    return user

def create_cart(db: Session, user_id:int):
    cart = Cart(user_id=user_id)
    db.add(cart)
    db.flush() 
    return cart

