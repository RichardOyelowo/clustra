from .base import BaseResponse 
from pydantic import BaseModel 
import uuid


class UserCreate(BaseModel):
    email: str
    full_name: str
    plain_password: str
    

class UserResponse(BaseResponse):
    id: uuid.UUID
    email: str
    full_name: str
    is_active: bool


class UserUpdate(BaseModel):
    email: str | None = None
    full_name: str | None = None
    password: str | None = None
    is_active: bool | None = None
