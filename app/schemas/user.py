from .base import BaseResponse 
from pydantic import BaseModel 
import uuid


class UserCreate(BaseModel):
    email: str
    username: str
    plain_password: str
    

class UserResponse(BaseResponse):
    id: uuid.UUID
    email: str
    username: str
    is_active: bool


class UserUpdate(BaseModel):
    email: str | None = None
    username: str | None = None
    password: str | None = None
    is_active: bool | None = None
