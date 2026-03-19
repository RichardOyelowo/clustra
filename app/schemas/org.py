from .base import BaseResponse
from pydantic import BaseModel
from datetime import datetime
import uuid


class OrganizationCreate(BaseModel):
    name: str
    slug: str
    desc: str | None = None


class OrganizationResponse(BaseResponse):
    id: uuid.UUID
    name: str
    slug: str
    owner_id: uuid.UUID
    desc: str | None


class OrganizationMemberCreate(BaseModel):
    user_id: uuid.UUID
    role: str = "member"


class OrganizationMemberResponse(BaseResponse):
    user_id: uuid.UUID
    role: str
    joined_at: datetime
