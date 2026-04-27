from ..models.project import ProjectStatus
from .base import BaseResponse
from pydantic import BaseModel
import uuid

class ProjectCreate(BaseModel):
    name: str
    desc: str | None = None
    team_id: uuid.UUID


class ProjectUpdate(BaseModel):
    name: str | None = None
    desc: str | None = None
    status: ProjectStatus | None = None


class ProjectResponse(BaseResponse):
    id: uuid.UUID
    name: str
    desc: str | None
    team_id: uuid.UUID
    status: ProjectStatus

