"""JWT token creation and decoding utilities."""

from datetime import UTC, datetime, timedelta

from jose import JWTError, jwt

from weather_app.settings import settings

secret_key = settings.secret_key
algorithm = settings.algorithm


def create_access_token(user_data: dict[str, object]) -> str:
    """Create a signed JWT token containing the given payload data."""
    payload = user_data.copy()
    expire = datetime.now(UTC) + timedelta(
        minutes=settings.access_token_expire_minutes,
    )
    payload.update({"exp": expire})
    return jwt.encode(payload, secret_key, algorithm=algorithm)


def decode_token(token: str) -> dict[str, object] | None:
    """Decode and verify a JWT token. Returns payload or None if invalid."""
    try:
        return jwt.decode(token, secret_key, algorithms=[algorithm])  # type: ignore[return-value]
    except JWTError:
        return None
