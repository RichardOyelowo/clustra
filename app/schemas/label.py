from .base import BaseResponse
from pydantic import BaseModel
import uuid


class LabelCreate(BaseModel):
    name: str
    color: str
    proj_id: uuid.UUID


class LabelResponse(BaseResponse):
    id: uuid.UUID
    name: str
    color: str
    proj_id: uuid.UUID


class TaskLabelCreate(BaseModel):
    label_id: uuid.UUID
    task_id: uuid.UUID


class TaskLabelResponse(BaseResponse):
    id: uuid.UUID
    label_id: uuid.UUID
    task_id: uuid.UUID
    
