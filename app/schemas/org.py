from ..models import OrganizationMemberRole
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


class OrganizationUpdate(BaseModel):
    id : uuid.UUID | None = None
    name: str | None = None
    slug: str | None = None
    owner_id: uuid.UUID | None = None
    desc: str | None = None



class OrganizationMemberCreate(BaseModel):
    user_id: uuid.UUID
    role: OrganizationMemberRole = OrganizationMemberRole.MEMBER


class OrganizationMemberResponse(BaseResponse):
    user_id: uuid.UUID
    role: OrganizationMemberRole
    joined_at: datetime
