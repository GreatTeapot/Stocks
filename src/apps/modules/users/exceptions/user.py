from fastapi import HTTPException
from modules.users.const import exceptions as exc



class UserNotFoundException(HTTPException):
    """Exception raised when a user is not found in the database."""

    def __init__(self) -> None:
        self.status_code = 404
        self.detail = exc.USER_NOT_FOUND
        super().__init__(status_code=self.status_code, detail=self.detail)


class EmailAlreadyExistsException(HTTPException):
    """Exception raised when an email already exists in the database."""

    def __init__(self) -> None:
        self.status_code = 409
        self.detail = exc.EMAIL_CONFLICT
        super().__init__(status_code=self.status_code, detail=self.detail)


class UsernameAlreadyExistsException(HTTPException):
    """Exception raised when a username already exists in the database."""

    def __init__(self) -> None:
        self.status_code = 409
        self.detail = exc.USERNAME_CONFLICT
        super().__init__(status_code=self.status_code, detail=self.detail)


class AuthUnauthorizedException(HTTPException):
    """Exception raised for invalid or expired authentication token."""

    def __init__(self) -> None:
        self.status_code = 401
        self.detail = exc.CREDENTIALS_CONFLICT
        self.headers = {"WWW-Authenticate": "Bearer"}
        super().__init__(
            status_code=self.status_code, detail=self.detail, headers=self.headers
        )


class AuthForbiddenException(HTTPException):
    """Exception raised for forbidden access."""

    def __init__(self, detail: str) -> None:
        self.status_code = 403
        self.detail = detail
        self.headers = {"WWW-Authenticate": "Bearer"}
        super().__init__(
            status_code=self.status_code, detail=self.detail, headers=self.headers
        )


class AuthNotFoundException(HTTPException):
    """Exception raised when required data is not found."""

    def __init__(self, detail: str) -> None:
        self.status_code = 404
        self.detail = detail
        self.headers = {"WWW-Authenticate": "Bearer"}
        super().__init__(
            status_code=self.status_code, detail=self.detail, headers=self.headers
        )


class AuthBadRequestException(HTTPException):
    """Exception raised for invalid request."""

    def __init__(self, detail: str) -> None:
        self.status_code = 400
        self.detail = detail
        self.headers = {"WWW-Authenticate": "Bearer"}
        super().__init__(
            status_code=self.status_code, detail=self.detail, headers=self.headers
        )