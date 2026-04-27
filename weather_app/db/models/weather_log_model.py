"""WeatherDetails database model."""

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from weather_app.db.base import Base

if TYPE_CHECKING:
    from weather_app.db.models.user_model import User


class WeatherDetails(Base):
    """Represents a saved weather record belonging to a user."""

    __tablename__ = "weather_details"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    city: Mapped[str] = mapped_column(String(200), nullable=False)
    country: Mapped[str] = mapped_column(String(10), nullable=False)
    temperature_c: Mapped[float] = mapped_column(Float, nullable=False)
    feels_like_c: Mapped[float] = mapped_column(Float, nullable=False)
    humidity: Mapped[int] = mapped_column(Integer, nullable=False)
    wind_speed_kmh: Mapped[float] = mapped_column(Float, default=0.0)
    visibility_m: Mapped[int] = mapped_column(Integer, nullable=False, default=10000)
    description: Mapped[str] = mapped_column(String(200), nullable=False)
    icon: Mapped[str] = mapped_column(String(50), nullable=False)
    saved_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    user: Mapped["User"] = relationship("User", back_populates="weather_logs")
