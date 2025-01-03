from typing import Optional

from pydantic import Field

from common.schemas.base import BaseModel


class TokenInfoSchema(BaseModel):
    """Schema for token information."""
    access_token: str
    token_type: str = Field(default="Bearer")


class LogoutResponseSchema(BaseModel):
    """Response on log out."""

    message: str = Field(default="You have successfully logged out.")


class EmptyUserSchema(BaseModel):
    """Empty user."""


class UserInfoSchema(BaseModel):
    """Schema for user information."""

    id: str
    username: str
    email: str
    deleted: bool
    role: Optional[str]