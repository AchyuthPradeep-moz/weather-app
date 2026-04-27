"""Authentication dependency: extract and validate current user from JWT."""

import uuid

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from weather_app.db.dao.user_dao import UserDAO
from weather_app.db.dependencies import get_db_session
from weather_app.db.models.user_model import User
from weather_app.services.jwt import decode_token

bearer = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer),
    db: AsyncSession = Depends(get_db_session),
) -> User:
    """Extract and validate the JWT from the Authorization header, return the user."""
    payload = decode_token(credentials.credentials)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
    user_dao = UserDAO(db)
    user = await user_dao.get_by_id(uuid.UUID(str(payload["sub"])))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    return user
