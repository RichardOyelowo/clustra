from pydantic import BaseModel 
import uuid


class UserCreate(BaseModel):
    email: str
    username: str
    plain_password: str
    


class UserResponse(BaseModel):
    id: uuid.UUID
    email: str
    username: str
    is_active: bool
