from .base import BaseResponse 
from pydantic import BaseModel 
import uuid


class UserCreate(BaseModel):
    email: str
    username: str
    plain_password: str
    

class UserResponse(BaseModel, BaseResponse):
    id: uuid.UUID
    email: str
    username: str
    is_active: bool
