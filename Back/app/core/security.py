from datetime import datetime, timedelta, timezone
from jose import jwt
from passlib.context import CryptContext
from app.core.settings import settings


pwd_context = CryptContext(schemes=['bcrypt'], deprecated ="auto")

ALGORITHM = "HS256"

def hash_password(password: str):
   return pwd_context.hash(password)


def verify_password(raw_password: str, hashed_password: str):
   return pwd_context.verify(raw_password,hashed_password)


def create_access_token(data: dict, expires_delta: timedelta = timedelta(hours=24)):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
   
