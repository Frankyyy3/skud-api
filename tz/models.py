import enum
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Direction(str, enum.Enum):
    IN = "IN"
    OUT = "OUT"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    events: Mapped[list["PassEvent"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )


class PassEvent(Base):
    __tablename__ = "pass_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    direction: Mapped[Direction] = mapped_column(
        Enum(Direction, native_enum=False, length=3),
        nullable=False,
    )
    user: Mapped[User] = relationship(back_populates="events")
