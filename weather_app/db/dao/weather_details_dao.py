"""DAO for WeatherDetails database operations."""

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from weather_app.db.models.weather_log_model import WeatherDetails


class WeatherDetailsDAO:
    """Handles all database operations for the WeatherDetails model."""

    def __init__(self, session: AsyncSession) -> None:
        """Initialise with an async database session."""
        self.session = session

    async def save(self, user_id: uuid.UUID, **data: object) -> WeatherDetails:
        """Save a weather record for a user. Commit is handled by get_db_session."""
        log = WeatherDetails(user_id=user_id, **data)
        self.session.add(log)
        await self.session.flush()
        await self.session.refresh(log)
        return log

    async def get_by_user(self, user_id: uuid.UUID) -> list[WeatherDetails]:
        """Return all saved weather records for a user, newest first."""
        result = await self.session.execute(
            select(WeatherDetails)
            .where(WeatherDetails.user_id == user_id)
            .order_by(WeatherDetails.saved_at.desc()),
        )
        return list(result.scalars().all())

    async def delete(self, log_id: int, user_id: uuid.UUID) -> bool:
        """Delete a weather record if it belongs to the given user."""
        log = await self.session.get(WeatherDetails, log_id)
        if not log or log.user_id != user_id:
            return False
        await self.session.delete(log)
        await self.session.flush()
        return True
