"""Pydantic schemas for auth endpoints."""

import uuid

from pydantic import BaseModel, EmailStr


class SignupRequest(BaseModel):
    """Data required to create a new user account."""

    email: EmailStr
    username: str
    password: str


class LoginRequest(BaseModel):
    """Data required to log in."""

    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """Response returned after a successful login."""

    access_token: str
    token_type: str = "bearer"  # noqa: S105
    username: str


class UserResponse(BaseModel):
    """Public-safe user profile (no password)."""

    id: uuid.UUID
    email: str
    username: str
