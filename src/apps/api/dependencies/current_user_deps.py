from datetime import datetime

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import DecodeError, ExpiredSignatureError, MissingRequiredClaimError
from core.config import settings
from core.security import Security
from modules.users.const import exceptions as exc
from modules.users.exceptions import user as error
from modules.users.schemas.auth import UserInfoSchema
from modules.users.unit_of_works.user import UserUOW

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=str(settings.auth.token_url), scheme_name="JWT"
)

class CurrentUserDep:
    """Dependency for retrieving the current user."""

    @staticmethod
    async def get_data_user(
        token: str, uow: UserUOW = None
    ) :
        """Retrieve user data."""
        try:
            payload = Security.decode_token(token)
        except ExpiredSignatureError:
            raise error.AuthForbiddenException(detail=exc.TOKEN_EXPIRED_FORBIDDEN)
        except DecodeError:
            raise error.AuthForbiddenException(detail=exc.TOKEN_INVALID_FORBIDDEN)
        except MissingRequiredClaimError:
            raise error.AuthForbiddenException(
                detail=exc.TOKEN_REQUIRED_FIELD_FORBIDDEN,
            )

        if datetime.fromtimestamp(payload.get("exp")) < datetime.now():
            raise error.AuthUnauthorizedException()
        login = payload.get("sub")
        if login is None:
            raise error.AuthUnauthorizedException()

        if uow is None:
            uow = UserUOW()
        async with uow:
            data_user = await uow.repo.get(login)

        if data_user is None:
            raise error.AuthUnauthorizedException()
        if data_user.deleted:
            raise error.AuthBadRequestException(detail=exc.USER_REMOVED_REQUEST)

        return data_user

    @classmethod
    async def get_current_user(
        cls,
        token: str = Depends(oauth2_scheme),
    ) -> UserInfoSchema:
        """Retrieve the current user."""
        response = await cls.get_data_user(token=token)
        user_info = UserInfoSchema(
            id=response.id,
            username=response.username,
            email=response.email,
            deleted=bool(response.deleted),
            role=response.role,
        )
        return user_info
