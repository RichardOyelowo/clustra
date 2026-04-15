from .base import BaseResponse
from pydantic import BaseModel
from uuid import UUID


class LabelCreate(BaseModel):
    name: str
    color: str
    proj_id: UUID


class LabelResponse(BaseResponse):
    id: UUID
    name: str
    color: str
    proj_id: UUID


class LabelUpdate(BaseModel):
    name: str | None = None
    color: str | None = None
    proj_id: UUID | None = None


class TaskLabelCreate(BaseModel):
    label_id: UUID
    task_id: UUID


class TaskLabelResponse(BaseResponse):
    id: UUID
    label_id: UUID
    task_id: UUID


class TaskLabelUpdate(BaseModel):
    label_id: UUID | None = None
    task_id: UUID | None = None
