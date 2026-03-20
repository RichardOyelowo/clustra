from ..models.activity import ActivityType, ModelType
from .base import BaseResponse
from pydantic import BaseModel
import uuid


class ActivityCreate(BaseModel):
    user_id: uuid.UUID
    action: ActivityType = ActivityType.CREATED
    model_type: ModelType = ModelType.ORGANIZATION
    model_id: uuid.UUID


class ActivityResponse(BaseResponse):
    id: uuid.UUID
    user_id: uuid.UUID
    action: ActivityType
    model_type: ModelType
    model_id: uuid.UUID
    org_id: uuid.UUID

