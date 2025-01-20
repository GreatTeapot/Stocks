
import uuid



from pydantic import Field

from modules.users.const import exceptions as exc
from common.schemas.base import BaseModel


class SuccessIdResponseSchema(BaseModel):
    """Response schema for successful user registration."""

    detail: str = Field(default=uuid.uuid4())


class SuccessBoolResponseSchema(BaseModel):
    """Response schema for successful operation execution."""

    detail: bool = Field(default=True)

class BadRequestResponseSchema(BaseModel):
    """Response schema for invalid request."""

    detail: str = Field(default=exc.INVALID_DATA_MESSAGE)


class UnauthorizedResponseSchema(BaseModel):
    """Response schema for an unauthorized request."""

    detail: str = Field(default=exc.UNAUTHORIZED_USER_MESSAGE)


class ForbiddenResponseSchema(BaseModel):
    """Response schema for access forbidden to the endpoint."""

    detail: str = Field(default=exc.NO_ACCESS_RIGHTS_MESSAGE)


class ForbiddenAdminResponseSchema(BaseModel):
    """Response schema for access forbidden to the endpoint with 'admin' role."""

    detail: str = Field(default=exc.ADMIN_ROLE_REQUIRED_MESSAGE)

class NotFoundResponseSchema(BaseModel):
    """Response schema for resource not found."""

    detail: str = Field(default=exc.DATA_NOT_FOUND_MESSAGE)


class UserNotFoundResponseSchema(BaseModel):
    """Response schema when the resource is not found"""

    detail: str = Field(default=exc.USER_NOT_FOUND)


class ServerErrorResponseSchema(BaseModel):
    """Response schema when unauthorized request"""

    detail: str = Field(default=exc.SERVER_ERROR_MESSAGE)
    

class UserBadRequestResponseSchema(BaseModel):
    """Response schema for invalid user request."""

    detail: str = Field(default=exc.USER_REMOVED_REQUEST)

