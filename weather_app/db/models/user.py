"""User database model."""

import uuid

from sqlalchemy import DateTime, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column, relationship

from weather_app.db.base import Base


class User(Base):
    """Represents a registered user account."""

    __tablename__ = "users"

    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = mapped_column(String(100), unique=True, nullable=False)
    email = mapped_column(String(255), unique=True, nullable=False)
    hashed_password = mapped_column(String(255), nullable=False)
    created_at = mapped_column(DateTime, server_default=func.now())

    weather_logs = relationship("WeatherDetails", back_populates="user")
