from ..models.milestone import MilestoneStatus
from .base import BaseResponse
from pydantic import BaseModel
from datetime import date
import uuid


class MilestoneCreate(BaseModel):
    title: str
    proj_id: uuid.UUID
    status: MilestoneStatus = MilestoneStatus.PENDING
    due_date: date | None = None


class MilestoneResponse(BaseResponse):
    id: uuid.UUID
    title: str
    proj_id: uuid.UUID
    status: MilestoneStatus
    due_date: date | None
    
