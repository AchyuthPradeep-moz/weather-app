"""Central API router — registers all feature routers."""

from fastapi.routing import APIRouter

from weather_app.web.api import echo, monitoring
from weather_app.web.api.auth import router as auth_router
from weather_app.web.api.weather import router as weather_router

api_router = APIRouter()

api_router.include_router(monitoring.router, tags=["monitoring"])
api_router.include_router(echo.router, prefix="/echo", tags=["echo"])
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(weather_router, prefix="/weather", tags=["weather"])
