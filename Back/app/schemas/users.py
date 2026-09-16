from pydantic import BaseModel, EmailStr,Field
from uuid import UUID


class UserResponse(BaseModel):
    public_id: UUID
    username:str
    email:EmailStr
    role:str
    
    model_config = {"from_attributes": True}
