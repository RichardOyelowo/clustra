from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import String, ForeignKey
from .base import Base, TimeStamp
import uuid
import enum


class ActivityType(str, enum.Enum):
    CREATED = "created"
    UPDATED= "updated"
    DELETED = "deleted"


class ModelType(str, enum.Enum):
    ORGANIZATION = "organization" 
    ORGANIZATION_MEMBER = "organization_member"
    USER = "user"
    TEAM = "team"
    PROJECT = "project"
    TASK = "task"
    MILESTONE = "milestone"


class Activity(Base, TimeStamp):
    __tablename__ = "activities"

    id: Mapped[uuid.UUID] = mapped_column(
            UUID(as_uuid=True),
            primary_key=True,
            default=uuid.uuid4,
            unique=True,
            nullable=False
    )
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"))
    action: Mapped[ActivityType] = mapped_column(String, default="created", nullable=False)
    model_type: Mapped[ModelType] = mapped_column(String, default="organization", nullable=False)
    model_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    org_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("organizations.id"))

