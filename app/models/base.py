from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime, timezone
from sqlalchemy import DateTime


class Base(DeclarativeBase):
    pass


class TimeStamp:
    created_at: Mapped[datetime] = mapped_column(
            DateTime(timezone=True), 
            default=lambda: datetime.now(timezone.utc), 
            nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column( 
            DateTime(timezone=True), 
            default=lambda: datetime.now(timezone.utc), 
            onupdate=lambda: datetime.now(timezone.utc), 
            nullabe=False
    )
