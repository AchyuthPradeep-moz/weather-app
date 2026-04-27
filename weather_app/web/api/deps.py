"""Re-export get_current_user from services for backwards compatibility."""

from weather_app.services.auth import get_current_user

__all__ = ["get_current_user"]
