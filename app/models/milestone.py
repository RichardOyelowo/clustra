from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, Date
from sqlalchemy.dialects.postgresql import UUID
from .base import Base, TimeStamp
from datetime import date
import uuid
import enum


class MilestoneStatus(str, enum.Enum):
    PENDING = "pending"
    STARTED = "started"
    COMPLETED = "completed"


class Milestone(Base, TimeStamp):
    __tablename__ = "milestones"

    id: Mapped[uuid.UUID] = mapped_column(
            UUID(as_uuid=True),
            primary_key=True,
            default=uuid.uuid4,
            unique=True,
            nullable=False,
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    proj_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("projects.id"))
    status: Mapped[MilestoneStatus] = mapped_column(String, default="pending", nullable=False)
    due_date: Mapped[date | None] = mapped_column(Date, default=date.today, nullable=True)

