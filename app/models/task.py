from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, Date
from sqlalchemy.dialects.postgresql import UUID
from .base import Base, TimeStamp
from datetime import date
import uuid
import enum


class TaskStatus(str, enum.Enum):
    COMPLETED = "completed"
    ACTIVE = "active"
    PENDING = "pending"
    ARCHIVED = "archived"
    CANCELLED = "cancelled"

class TaskPriority(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Task(Base, TimeStamp):
    __tablename__ = "tasks"

    id: Mapped[uuid.UUID] = mapped_column(
            UUID(as_uuid=True), 
            primary_key=True, 
            default=uuid.uuid4,
            unique=True,
            nullable=False
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    desc: Mapped[str | None] = mapped_column(String(500), nullable=True)
    status: Mapped[TaskStatus] = mapped_column(String, default="pending", nullable=False)
    priority: Mapped[TaskPriority] = mapped_column(String, default="low", nullable=False)
    proj_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)
    assignee_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    due_date: Mapped[date | None] = mapped_column(Date, default=date.today, nullable=True)


    def __repr__(self) -> str:
        return f"<Task id: {self.id} fro Project: {self.proj_id}>"
