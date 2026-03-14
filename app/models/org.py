from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, timezone
from .base import Base, TimeStamp
import uuid


class Organization(Base, TimeStamp):
    __tablename__ = "organizations"

    id: Mapped[uuid.UUID] = mapped_column(
            UUID(as_uuid=True), 
            primary_key=True, 
            default=uuid.uuid4,
            unique=True,
            nullable=False
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    slug: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    owner_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    desc: Mapped[str | None] = mapped_column(String(500), nullable=True)

    def __repr__(self) -> str:
        return f"<{name}, Organization id: {self.id}>"


class OrganizationMember(Base):
    __tablename__ = "organizationmembers"

    id: Mapped[uuid.UUID] = mapped_column(
            UUID(as_uuid=True), 
            primary_key=True,
            default=uuid.uuid4, 
            unique=True, 
            nullable=False
    )
    org_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("organizations.id"))
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"))
    role: Mapped[str] = mapped_column(String(100), default="member")
    joined_at: Mapped[datetime] = mapped_column(DateTime,default=lambda: datetime.now(timezone.utc))

    def __repr__(self) -> str:
        return f"<Organization Member: {self.id} from organization: {self.org_id}>"
