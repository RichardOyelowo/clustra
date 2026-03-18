from .base import BaseResponse
from pydantic import BaseModel
from datetime import datetime
import uuid


class OrganizationCreate(BaseModel):
    name: str
    slug: str
    owner_id: uuid.UUID
    desc: str


class OrganizationResponse(BaseModel):
    id: uuid.UUID
    name: str
    slug: str
    owner_id: uuid.UUID
    desc: str


class OrganizationMemberCreate(BaseModel):
    org_id: uuid.UUID
    user_id: uuid.UUID
    role: str


class OrganizationMemberResponse(BaseModel):
    org_id: uuid.UUID
    user_id: uuid.UUID
    role: str
    joined_at: datetime
