"""Weather endpoints."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from weather_app.db.dependencies import get_db_session
from weather_app.db.models.user import User
from weather_app.db.models.weather_log import WeatherDetails
from weather_app.services.weather import fetch_weather
from weather_app.web.api.deps import get_current_user
from weather_app.web.api.weather.schema import SavedWeatherResponse, WeatherResponse

router = APIRouter(tags=["weather"])


@router.get("/search", response_model=WeatherResponse)
async def search_weather(
    city: str,
    current_user: User = Depends(get_current_user),
) -> dict[str, object]:
    """Fetch live weather for a city. Requires authentication."""
    data = await fetch_weather(city)
    if "error" in data:
        raise HTTPException(status_code=404, detail=data["error"])
    return data


@router.post("/save", response_model=SavedWeatherResponse, status_code=201)
async def save_weather(
    city: str,
    db: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
) -> WeatherDetails:
    """Fetch weather for a city and save it to the current user's history."""
    data = await fetch_weather(city)
    if "error" in data:
        raise HTTPException(status_code=404, detail=data["error"])

    log = WeatherDetails(user_id=current_user.id, **data)
    db.add(log)
    await db.commit()
    await db.refresh(log)
    return log


@router.get("/history", response_model=list[SavedWeatherResponse])
async def get_weather_history(
    db: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
) -> list[WeatherDetails]:
    """Return all saved weather records for the current user, newest first."""
    result = await db.execute(
        select(WeatherDetails)
        .where(WeatherDetails.user_id == current_user.id)
        .order_by(WeatherDetails.saved_at.desc()),
    )
    return list(result.scalars().all())


@router.delete("/history/{log_id}", status_code=204)
async def delete_weather_log(
    log_id: int,
    db: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
) -> None:
    """Delete a specific saved weather entry belonging to the current user."""
    log = await db.get(WeatherDetails, log_id)
    if not log or log.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Record not found")
    await db.delete(log)
    await db.commit()
