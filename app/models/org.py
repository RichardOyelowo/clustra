from sqlalchemy import ForeignKey, String, DateTime, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID, ENUM
from datetime import datetime, timezone
from .base import Base, TimeStamp
import uuid
import enum

class OrganizationMemberRole(str, enum.Enum):
    OWNER = "owner"
    ADMIN = "admin"
    MEMBER = "member"

    
class Organization(Base, TimeStamp):
    __tablename__ = "organizations"
    __table_args__ = (
        UniqueConstraint("slug", name="uq_organization_slug")
    )

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
        return f"<{self.name}, Organization id: {self.id}>"


class OrganizationMember(Base):
    __tablename__ = "organizationmembers"
    __table_args__ = (
        UniqueConstraint("org_id", "user_id", name="uq_org_member_user")
    )

    id: Mapped[uuid.UUID] = mapped_column(
            UUID(as_uuid=True), 
            primary_key=True,
            default=uuid.uuid4, 
            unique=True, 
            nullable=False
    )
    org_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("organizations.id"))
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"))
    role: Mapped[OrganizationMemberRole] = mapped_column(ENUM(OrganizationMemberRole), default=OrganizationMemberRole.MEMBER, nullable=False)
    joined_at: Mapped[datetime] = mapped_column(DateTime,default=lambda: datetime.now(timezone.utc))

    def __repr__(self) -> str:
        return f"<Organization Member: {self.id} from organization: {self.org_id}>"
