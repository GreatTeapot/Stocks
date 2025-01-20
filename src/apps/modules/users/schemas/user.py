
from datetime import datetime
from typing import Optional, TypeVar
from uuid import UUID

from pydantic import EmailStr, Field, field_validator
from pydantic.json_schema import SkipJsonSchema as HiddenField

from common.enums.role import UserRoleEnum
from common.schemas.base import BaseModel

TSchema = TypeVar("TSchema", bound=BaseModel)

class UserResponseSchema(BaseModel):
    """Schema of the user response."""
    id: UUID
    username: str
    email: EmailStr
    last_name: Optional[str]
    first_name: Optional[str]
    photo: Optional[str] = Field(default=None)

class CurrentUserSchema(UserResponseSchema):
    """Schema of the current user."""

    role: str


class PersonBaseSchema(BaseModel):
    """Base schema for a person."""

    id: UUID
    username: str
    email: EmailStr

class PersonSchema(PersonBaseSchema):
    """Schema for a person."""


class RegisterSchema(BaseModel):
    """General schema for registration"""

    role: HiddenField[UserRoleEnum] = Field(default=UserRoleEnum.USER)
    username: str
    email: EmailStr
    password_hash: str
    created_at: HiddenField[datetime] = Field(default=datetime.now())
    updated_at: HiddenField[datetime] = Field(default=datetime.now())

    @field_validator("username")
    def validate_username(cls, username: str) -> str:
        """Username validation."""
        if len(username) < 3:
            raise ValueError("Username must be at least 3 characters long.")
        if not username.isalnum():
            raise ValueError("Username must only contain letters and digits.")
        return username

    @field_validator("password_hash")
    def validate_password(cls, password: str) -> str:  # noqa
        """Password validation."""
        if not password or len(password) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        if not password.isalnum():
            raise ValueError("Password must consist of only letters and digits.")
        if not any(c.isdigit() for c in password) or not any(c.isalpha() for c in password):
            raise ValueError("Password must contain at least one letter and one digit.")
        return password
      


class UpdateUserSchema(BaseModel):
    """General schema for updates"""

    last_name: str
    first_name: str
    photo: Optional[str] = Field(default=None)
    updated_at: HiddenField[datetime] = Field(default=datetime.now())

    @field_validator("last_name")
    def validate_last_name(cls, last_name: str) -> str:  # noqa
        """Validation of the last name."""
        if 2 <= len(last_name) <= 50:
            return last_name
        raise ValueError("The number of characters in the last name must be more than 1 and less than 51.")

    @field_validator("first_name")
    def validate_first_name(cls, first_name: str) -> str:  # noqa
        """Validation of the first name."""
        if 2 <= len(first_name) <= 50:
            return first_name
        raise ValueError("The number of characters in the first name must be more than 1 and less than 51.")

