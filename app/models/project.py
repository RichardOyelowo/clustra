from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import String, ForeignKey
from .base import Base, TimeStamp
import uuid
import enum


class ProjectStatus(str, enum.Enum):
    COMPLETED = "completed"
    ACTIVE = "active"
    PENDING = "pending"
    ARCHIVED = "archived"
    CANCELLED = "cancelled"


class Project(Base, TimeStamp):
    __tablename__ = "projects"

    id: Mapped[uuid.UUID] = mapped_column(
            UUID(as_uuid=True), 
            primary_key=True,
            default=uuid.uuid4, 
            unique=True,
            nullable=False
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    desc: Mapped[str | None] = mapped_column(String(500), nullable=True)
    team_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("teams.id"), nullable=False)
    org_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False)
    status: Mapped[ProjectStatus] = mapped_column(String, default="pending", nullable=False)

    def __repr__(self) -> str:
        return f"<Project id: {self.id}>"

