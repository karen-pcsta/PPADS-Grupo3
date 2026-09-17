from http.client import HTTPException

from app.core.settings import settings
from app.schemas.users import UserResponse
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.auth import AuthLoginResponse, AuthRegister, AuthLogin
from app.services import auth_service
from app.core.dependencies import get_db, verify_jwt

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model = AuthLoginResponse, status_code=201)
def auth_register(auth_data: AuthRegister, db: Session = Depends(get_db)):
    return auth_service.register(db,auth_data)

@router.post("/login", response_model = AuthLoginResponse, status_code=200)
def auth_login(auth_data: AuthLogin, db: Session = Depends(get_db)):
    return auth_service.login(db,auth_data)


@router.post("/logout", status_code=200)
def logout(current_user = Depends(verify_jwt)):
    return {"detail": "Logged out successfully"}


@router.get("/me", response_model=UserResponse, status_code=200)
def me(current_user = Depends(verify_jwt)):
    return current_user

