"""Password hashing and verification utilities."""

from passlib.context import CryptContext

pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a plaintext password using bcrypt."""
    return pwd.hash(password)  # type: ignore[return-value]


def verify_password(password: str, hashed: str) -> bool:
    """Check a plaintext password against a stored bcrypt hash."""
    return pwd.verify(password, hashed)  # type: ignore[return-value]
