from ..models.task import TaskPriority, TaskStatus
from .base import BaseResponse
from pydantic import BaseModel
from datetime import date
import uuid


class TaskCreate(BaseModel):
    name: str
    desc: str | None = None
    status: TaskStatus = TaskStatus.PENDING
    priority: TaskPriority = TaskPriority.LOW
    proj_id: uuid.UUID
    assignee_id: uuid.UUID | None = None
    due_date: date | None = None


class TaskUpdate(BaseModel):
    name: str | None = None
    desc: str | None = None
    status: TaskStatus | None = None
    priority: TaskPriority | None = None
    assignee_id: uuid.UUID | None = None
    due_date: date | None = None


class TaskResponse(BaseResponse):
    id: uuid.UUID
    name: str
    desc: str | None
    status: TaskStatus
    priority: TaskPriority
    proj_id: uuid.UUID
    assignee_id: uuid.UUID | None
    due_date: date | None
