from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import String, Boolean
from .base import Base, TimeStamp
import uuid


class User(Base, TimeStamp):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
            UUID(as_uuid=True), 
            primary_key=True, 
            default=uuid.uuid4,
            unique=True, 
            nullable=False
    )
    email: Mapped[str] = mapped_column(String(300), unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String(60), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    @property
    def hashed_password(self):
        return self.password_hash


    def __repr__(self) -> str:
        return f"<User id: {self.id}, email: {self.email}>"
