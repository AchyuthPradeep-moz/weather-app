"""WeatherDetails database model."""

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column, relationship

from weather_app.db.base import Base


class WeatherDetails(Base):
    """Represents a saved weather record belonging to a user."""

    __tablename__ = "weather_details"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    city = mapped_column(String(200), nullable=False)
    country = mapped_column(String(10), nullable=False)
    temperature_c = mapped_column(Float, nullable=False)
    feels_like_c = mapped_column(Float, nullable=False)
    humidity = mapped_column(Integer, nullable=False)
    wind_speed_kmh = mapped_column(Float, default=0.0)
    visibility_m = mapped_column(Integer, nullable=False, default=10000)
    description = mapped_column(String(200), nullable=False)
    icon = mapped_column(String(50), nullable=False)
    saved_at = mapped_column(DateTime, server_default=func.now())

    user = relationship("User", back_populates="weather_logs")
