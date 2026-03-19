from  ..models.team import TeamRole
from .base import BaseResponse
from pydantic import BaseModel
from datetime import datetime
import uuid


class TeamCreate(BaseModel):
    name: str
    slug: str
    desc: str | None = None


class TeamResponse(BaseResponse):
    id: uuid.UUID
    name: str
    slug: str
    desc: str | None


class TeamMemberCreate(BaseModel):
    user_id: uuid.UUID
    role: TeamRole = TeamRole.CONTRIBUTOR 


class TeamMemberResponse(BaseResponse):
    id: uuid.UUID
    role: TeamRole
    joined_at: datetime
