from sqlalchemy.orm import Session
from app.repositories import user_repository
from app.schemas.auth import AuthRegister, AuthLogin
from app.core.security import hash_password,verify_password, create_access_token
from app.core.exceptions import BadRequestException, ConflictException, UnauthorizedException


def register(db: Session, auth_data: AuthRegister):
    if user_repository.get_by_username(db,auth_data.username):
        raise ConflictException('Username already exists')
    if user_repository.get_by_email(db,auth_data.email):
        raise ConflictException('Email already exists')
    
    hashed_pw = hash_password(auth_data.password)

    user_data = auth_data.model_dump()
    user_data["password"] = hashed_pw

    user = user_repository.create_new_user(db, user_data)
    user_repository.create_cart(db,user.id)

    db.commit()
    db.refresh(user)

    access_token = create_access_token({
    "sub": str(user.public_id)
})

    return {"access_token": access_token, "token_type": "bearer"}


def login(db: Session, auth_data: AuthLogin):
    if not auth_data.username and not auth_data.email:
        raise BadRequestException('Username or email is required')

    if auth_data.username:
        user = user_repository.get_by_username(db, auth_data.username)
    elif auth_data.email:
        user = user_repository.get_by_email(db, auth_data.email)

    if not user:
        raise UnauthorizedException('Invalid credentials')
    
    if not verify_password(auth_data.password, user.password):
        raise UnauthorizedException('Invalid credentials')
    
    access_token = create_access_token({
    "sub": str(user.public_id)
})

    return {"access_token": access_token, "token_type": "bearer"}
