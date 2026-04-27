from datetime import datetime

from pydantic import BaseModel


class WeatherResponse(BaseModel):
    """The live data we show after a search."""

    city: str
    country: str
    temperature_c: float
    feels_like_c: float
    humidity: int
    wind_speed_kmh: float
    visibility_m: int  # Added this weather parameter we discussed!
    description: str
    icon: str  # The emoji icon


class SavedWeatherResponse(WeatherResponse):
    """Data for the 'History' page."""

    id: int  # Changed to int because we switched Weather logs to Integers
    saved_at: datetime
