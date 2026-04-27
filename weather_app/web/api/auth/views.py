"""Auth endpoints: signup and login."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from weather_app.db.dependencies import get_db_session
from weather_app.db.models.user import User
from weather_app.services.jwt import create_access_token
from weather_app.services.password import hash_password, verify_password
from weather_app.web.api.auth.schema import (
    LoginRequest,
    SignupRequest,
    TokenResponse,
    UserResponse,
)

router = APIRouter(tags=["auth"])


@router.post("/signup", response_model=UserResponse, status_code=201)
async def signup(
    body: SignupRequest,
    db: AsyncSession = Depends(get_db_session),
) -> User:
    """Register a new user account."""
    existing = await db.scalar(select(User).where(User.email == body.email))
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        email=body.email,
        username=body.username,
        hashed_password=hash_password(body.password),
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


@router.post("/login", response_model=TokenResponse)
async def login(
    body: LoginRequest,
    db: AsyncSession = Depends(get_db_session),
) -> dict[str, str]:
    """Log in and return a JWT access token."""
    user = await db.scalar(select(User).where(User.email == body.email))
    if not user or not verify_password(body.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    token = create_access_token({"sub": str(user.id), "username": user.username})
    return {"access_token": token, "token_type": "bearer", "username": user.username}
