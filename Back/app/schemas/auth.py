from typing import Optional
from pydantic import BaseModel, EmailStr,Field

class AuthRegister(BaseModel):
    username: str = Field(min_length=3, max_length=20)
    email:EmailStr
    password: str = Field(min_length=8)


class AuthLogin(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: str

class AuthLoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    
    model_config = {"from_attributes": True}