from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, timezone
from .base import Base, TimeStamp
import uuid
import enum


class TeamRole(str, enum.Enum):
    VIEWER = "viewer"
    CONTRIBUTOR = "contributor"
    LEAD = "lead"
    

class Team(Base, TimeStamp):
    __tablename__ = "teams"

    id: Mapped[uuid.UUID] = mapped_column(
            UUID(as_uuid=True), 
            primary_key=True, 
            default=uuid.uuid4,
            unique=True,
            nullable=False
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    slug: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    org_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False)
    desc: Mapped[str | None] = mapped_column(String(500), nullable=True)

    def __repr__(self) -> str:
        return f"<Team: {self.id}, Organization id: {self.org_id}>"


class TeamMember(Base):
    __tablename__ = "teammembers"

    id: Mapped[uuid.UUID] = mapped_column(
            UUID(as_uuid=True), 
            primary_key=True,
            default=uuid.uuid4, 
            unique=True, 
            nullable=False
    )
    team_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("teams.id"))
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"))
    role: Mapped[TeamRole] = mapped_column(String(100), default="contributor")
    joined_at: Mapped[datetime] = mapped_column(DateTime,default=lambda: datetime.now(timezone.utc))

    def __repr__(self) -> str:
        return f"<Team Member: {self.id} from team: {self.team_id}>"

