from sqlalchemy.orm import Session
from fastapi import HTTPException,Depends
from fastapi.security import HTTPBearer
from jose import jwt, JWTError
from app.database.session import SessionLocal
from app.core.settings import settings
from app.repositories import user_repository


security = HTTPBearer()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def verify_jwt(credentials = Depends(security), db: Session = Depends(get_db)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        public_id = payload.get("sub")
        if public_id is None:
            raise HTTPException(status_code=401, detail='Invalid credentials')
        user = user_repository.get_by_public_id(db, public_id)
    except JWTError:
        raise HTTPException(status_code=401, detail='Invalid credentials')
    return user


def verify_admin(current_user = Depends(verify_jwt)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail='Not authorized')
    return current_user



