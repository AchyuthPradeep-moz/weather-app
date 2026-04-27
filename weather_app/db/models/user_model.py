"""User database model."""

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from weather_app.db.base import Base

if TYPE_CHECKING:
    from weather_app.db.models.weather_log_model import WeatherDetails


class User(Base):
    """Represents a registered user account."""

    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    username: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())

    weather_logs: Mapped[list["WeatherDetails"]] = relationship(
        "WeatherDetails", back_populates="user"
    )
