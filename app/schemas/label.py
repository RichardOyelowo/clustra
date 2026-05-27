from .base import BaseResponse
from pydantic import BaseModel
from uuid import UUID


class LabelCreate(BaseModel):
    name: str
    color: str


class LabelResponse(BaseResponse):
    id: UUID
    name: str
    color: str
    proj_id: UUID
    team_id: UUID
    org_id: UUID


class LabelUpdate(BaseModel):
    name: str | None = None
    color: str | None = None


class TaskLabelCreate(BaseModel):
    task_id: UUID


class TaskLabelResponse(BaseResponse):
    id: UUID
    label_id: UUID
    task_id: UUID

