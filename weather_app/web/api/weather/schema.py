"""Pydantic schemas for weather endpoints."""

from datetime import datetime

from pydantic import BaseModel


class WeatherResponse(BaseModel):
    """Live weather data returned after a search."""

    city: str
    country: str
    temperature_c: float
    feels_like_c: float
    humidity: int
    wind_speed_kmh: float
    visibility_m: int
    description: str
    icon: str


class SavedWeatherResponse(WeatherResponse):
    """Saved weather record returned from history."""

    id: int
    saved_at: datetime
    model_config = {"from_attributes": True}  # required for ORM serialization
