from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from .base import Base, TimeStamp
import uuid


class Label(Base, TimeStamp):
    __tablename__ = "labels"
    __table_args__ = (UniqueConstraint("name", "proj_id", name="uq_label_per_project"),)

    id: Mapped[uuid.UUID] = mapped_column(
            UUID(as_uuid=True),
            primary_key=True,
            default=uuid.uuid4, 
            unique=True, 
            nullable=False
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    color: Mapped[str] = mapped_column(String, nullable=False)
    proj_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("projects.id"))


class TaskLabel(Base, TimeStamp):
    __tablename__ = "tasklabels"
    __table_args__ = (UniqueConstraint("label_id", "task_id", name="uq_tasklabel_per_task"),)

    id: Mapped[uuid.UUID] = mapped_column(
            UUID(as_uuid=True), 
            primary_key=True,
            default=uuid.uuid4,
            unique=True,
            nullable=False
    )
    label_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("labels.id"))
    task_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("tasks.id"))
