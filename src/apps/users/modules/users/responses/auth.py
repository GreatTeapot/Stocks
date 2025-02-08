from common.schemas.responses import mixins as response
from modules.users.const import exceptions as exc

LOGIN_RESPONSES = {
    400: {
        "description": "Bad Request",
        "content": {
            "application/json": {
                "examples": {
                    "Credentials bad request": {
                        "summary": "Credentials bad request",
                        "value": {"detail": exc.CREDENTIALS_BAD_REQUEST},
                    },
                    "user_bad_request": {
                        "summary": "User bad request",
                        "value": {"detail": exc.USER_BAD_REQUEST},
                    },
                }
            }
        },
    },
    500: {"model": response.ServerErrorResponseSchema},
}

REFRESH_RESPONSES = {
    400: {
        "description": "Bad Request",
        "content": {
            "application/json": {
                "examples": {
                    "user_bad_request": {
                        "summary": "User bad request",
                        "value": {"detail": exc.USER_BAD_REQUEST},
                    },
                    "token_bad_request": {
                        "summary": "Token bad request",
                        "value": {"detail": exc.TOKEN_BAD_REQUEST},
                    },
                }
            }
        },
    },
    500: {"model": response.ServerErrorResponseSchema},
}

AUTH_RESPONSES = {
    400: {"model": response.UserBadRequestResponseSchema},
    401: {"model": response.UnauthorizedResponseSchema},
    403: {
        "description": "Forbidden",
        "content": {
            "application/json": {
                "examples": {
                    "token_expired_forbidden": {
                        "summary": "Token expired forbidden",
                        "value": {"detail": exc.TOKEN_EXPIRED_FORBIDDEN},
                    },
                    "token_invalid_forbidden": {
                        "summary": "Token invalid forbidden",
                        "value": {"detail": exc.TOKEN_INVALID_FORBIDDEN},
                    },
                    "token_required_field_forbidden": {
                        "summary": "Token required field forbidden",
                        "value": {"detail": exc.TOKEN_REQUIRED_FIELD_FORBIDDEN},
                    },
                    "roles_forbidden": {
                        "summary": "Roles forbidden",
                        "value": {"detail": exc.ROLES_FORBIDDEN},
                    },
                }
            }
        },
    },
    500: {"model": response.ServerErrorResponseSchema},
}