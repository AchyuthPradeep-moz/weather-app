"""Open-Meteo weather client (no API key required)."""

import httpx

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

WMO_CODES: dict[int, tuple[str, str]] = {
    0: ("Clear sky", "☀️"),
    1: ("Mainly clear", "🌤️"),
    2: ("Partly cloudy", "⛅"),
    3: ("Overcast", "☁️"),
    45: ("Foggy", "🌫️"),
    48: ("Icy fog", "🌫️"),
    51: ("Light drizzle", "🌦️"),
    53: ("Moderate drizzle", "🌦️"),
    55: ("Dense drizzle", "🌧️"),
    61: ("Slight rain", "🌧️"),
    63: ("Moderate rain", "🌧️"),
    65: ("Heavy rain", "🌧️"),
    71: ("Slight snow", "🌨️"),
    73: ("Moderate snow", "❄️"),
    75: ("Heavy snow", "❄️"),
    77: ("Snow grains", "❄️"),
    80: ("Slight showers", "🌦️"),
    81: ("Moderate showers", "🌧️"),
    82: ("Violent showers", "⛈️"),
    85: ("Slight snow showers", "🌨️"),
    86: ("Heavy snow showers", "❄️"),
    95: ("Thunderstorm", "⛈️"),
    96: ("Thunderstorm with hail", "⛈️"),
    99: ("Thunderstorm with heavy hail", "⛈️"),
}


async def fetch_weather(city: str) -> dict[str, object]:
    """Fetch current weather for a city using Open-Meteo."""
    async with httpx.AsyncClient(timeout=10) as client:
        geo_resp = await client.get(
            GEOCODING_URL,
            params={"name": city, "count": 1, "language": "en", "format": "json"},
        )

        if geo_resp.status_code != 200:
            raise ValueError("Geocoding service unavailable")

        geo_data = geo_resp.json()
        results = geo_data.get("results")
        if not results:
            raise ValueError(f"City '{city}' not found")

        location = results[0]
        lat = location["latitude"]
        lon = location["longitude"]
        city_name = location["name"]
        country = location.get("country_code", "").upper()

        weather_resp = await client.get(
            WEATHER_URL,
            params={
                "latitude": lat,
                "longitude": lon,
                "current": [
                    "temperature_2m",
                    "apparent_temperature",
                    "relative_humidity_2m",
                    "weather_code",
                    "wind_speed_10m",
                    "visibility",
                ],
                "wind_speed_unit": "kmh",
                "temperature_unit": "celsius",
                "timezone": "auto",
            },
        )

        if weather_resp.status_code != 200:
            raise ValueError("Weather service unavailable")

        w = weather_resp.json()["current"]
        wmo_code = w["weather_code"]
        description, icon = WMO_CODES.get(wmo_code, ("Unknown", "🌡️"))

        return {
            "city": city_name,
            "country": country,
            "temperature_c": round(w["temperature_2m"], 1),
            "feels_like_c": round(w["apparent_temperature"], 1),
            "humidity": w["relative_humidity_2m"],
            "wind_speed_kmh": round(w["wind_speed_10m"], 1),
            "visibility_m": int(w.get("visibility", 10000)),
            "description": description,
            "icon": icon,
        }
