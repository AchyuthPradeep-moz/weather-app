"""DAO for User database operations."""

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from weather_app.db.models.user_model import User


class UserDAO:
    """Handles all database operations for the User model."""

    def __init__(self, session: AsyncSession) -> None:
        """Initialise with an async database session."""
        self.session = session

    async def get_by_email(self, email: str) -> User | None:
        """Return a user matching the given email, or None if not found."""
        return await self.session.scalar(select(User).where(User.email == email))

    async def get_by_id(self, user_id: uuid.UUID) -> User | None:
        """Return a user matching the given UUID, or None if not found."""
        return await self.session.get(User, user_id)

    async def create(
        self,
        email: str,
        username: str,
        hashed_password: str,
    ) -> User:
        """Create and flush a new user record. Commit is handled by get_db_session."""
        user = User(email=email, username=username, hashed_password=hashed_password)
        self.session.add(user)
        await self.session.flush()
        await self.session.refresh(user)
        return user
