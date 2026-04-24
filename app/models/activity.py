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
    ORGANIZATIONS = "organizations" 
    ORGANIZATION_MEMBERS = "organization_members"
    USERS = "users"
    TEAMS = "teams"
    TEAMMEMBERS = "teammembers"
    PROJECTS = "projects"
    TASKS = "tasks"
    TASKLABELS = "tasklabels"
    MILESTONES = "milestones"


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

