from common.schemas.responses import mixins as response
from modules.users.schemas.user import UserResponseSchema

REGISTRATION_RESPONSES = {
    200: {"model": response.SuccessIdResponseSchema},
    400: {"model": response.BadRequestResponseSchema},
    401: {"model": response.UnauthorizedResponseSchema},
    409: {
        "description": "Conflict",
        "content": {
            "application/json": {
                "examples": {
                    "email_conflict": {
                        "summary": "Email already exists",
                        "value": {"detail": "This email already exists."},
                    },
                    "username_conflict": {
                        "summary": "Username already exists",
                        "value": {"detail": "This username already exists."},
                    },

                }
            }
        },
    },
    500: {"model": response.ServerErrorResponseSchema},
}

GET_RESPONSES = {
    200: {"model": UserResponseSchema},
    401: {"model": response.UnauthorizedResponseSchema},
    500: {"model": response.ServerErrorResponseSchema},
}

GET_PUBLIC_RESPONSES = {
    200: {"model": UserResponseSchema},
    500: {"model": response.ServerErrorResponseSchema},
}

EDIT_RESPONSES = {
    200: {
        "description": "Successful Response",
        "content": {"application/json": {"example": True}},
    },
    401: {"model": response.UnauthorizedResponseSchema},
    403: {"model": response.ForbiddenResponseSchema},
    500: {"model": response.ServerErrorResponseSchema},
}