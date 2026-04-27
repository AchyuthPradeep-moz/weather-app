"""Weather endpoints."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from weather_app.db.dao.weather_details_dao import WeatherDetailsDAO
from weather_app.db.dependencies import get_db_session
from weather_app.db.models.user_model import User
from weather_app.db.models.weather_log_model import WeatherDetails
from weather_app.services.auth import get_current_user
from weather_app.services.weather import fetch_weather
from weather_app.web.api.weather.schema import SavedWeatherResponse, WeatherResponse

router = APIRouter(tags=["weather"])


@router.get("/search", response_model=WeatherResponse)
async def search_weather(
    city: str,
    current_user: User = Depends(get_current_user),
) -> dict[str, object]:
    """Fetch live weather for a city. Requires authentication."""
    try:
        return await fetch_weather(city)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


@router.post("/save", response_model=SavedWeatherResponse, status_code=201)
async def save_weather(
    city: str,
    db: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
) -> WeatherDetails:
    """Fetch weather for a city and save it to the current user's history."""
    try:
        data = await fetch_weather(city)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e

    weather_dao = WeatherDetailsDAO(db)
    return await weather_dao.save(user_id=current_user.id, **data)


@router.get("/history", response_model=list[SavedWeatherResponse])
async def get_weather_history(
    db: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
) -> list[WeatherDetails]:
    """Return all saved weather records for the current user, newest first."""
    weather_dao = WeatherDetailsDAO(db)
    return await weather_dao.get_by_user(current_user.id)


@router.delete("/history/{log_id}", status_code=204)
async def delete_weather_log(
    log_id: int,
    db: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
) -> None:
    """Delete a specific saved weather entry belonging to the current user."""
    weather_dao = WeatherDetailsDAO(db)
    deleted = await weather_dao.delete(log_id=log_id, user_id=current_user.id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Record not found")
