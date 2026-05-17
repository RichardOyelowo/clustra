import uuid

from pydantic import BaseModel

from ..models.activity import ActivityType, ModelType
from .base import BaseResponse


class ActivityCreate(BaseModel):
    user_id: uuid.UUID
    action: ActivityType = ActivityType.CREATED
    model_type: ModelType = ModelType.ORGANIZATIONS
    model_id: uuid.UUID


class ActivityResponse(BaseResponse):
    id: uuid.UUID
    user_id: uuid.UUID
    action: ActivityType
    model_type: ModelType
    model_id: uuid.UUID
    org_id: uuid.UUID
