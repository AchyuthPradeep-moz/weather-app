"""weather_app models."""

import pkgutil
from pathlib import Path

from weather_app.db.models.user import User
from weather_app.db.models.weather_log import WeatherDetails


def load_all_models() -> None:
    """Load all models from this folder."""
    package_dir = Path(__file__).resolve().parent
    modules = pkgutil.walk_packages(
        path=[str(package_dir)],
        prefix="weather_app.db.models.",
    )
    for module in modules:
        __import__(module.name)


__all__ = ["User", "WeatherDetails", "load_all_models"]
