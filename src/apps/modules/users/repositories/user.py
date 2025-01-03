from datetime import datetime
from types import NoneType
from typing import Optional, TypeAlias, Union
from uuid import UUID

import sqlalchemy as sa

from common.enums.role import UserRoleEnum
from common.repositories.mixins import PaginatedPageRepository
from models.users import User
from modules.users.exceptions import user as exc

RegisterData: TypeAlias = dict[str, Union[str, datetime, bool, UserRoleEnum, NoneType, UUID]]
EditData: TypeAlias = dict[str, Union[UUID, str, bool, datetime, int, None, UserRoleEnum]]


class UserRepository(PaginatedPageRepository):
    """User profile repository."""

    model = User

    async def __is_exist_email(self, user_email: str) -> bool:
        """Check for the existence of a user with the given email in the database."""
        stmt = sa.select(self.model).filter(self.model.email.ilike(user_email))
        result = (await self.session.execute(stmt)).scalar_one_or_none()
        return bool(result)

    async def __is_exist_username(self, username: str) -> bool:
        """Check for the existence of a user with the given username in the database."""
        stmt = sa.select(self.model).filter(self.model.username.ilike(username))
        result = (await self.session.execute(stmt)).scalar_one_or_none()
        return bool(result)

    async def add(self, data: RegisterData) -> str:
        """Add a new user profile entry to the database."""
        if await self.__is_exist_email(data["email"]):
            raise exc.EmailAlreadyExistsException()

        if await self.__is_exist_username(data["username"]):
            raise exc.UsernameAlreadyExistsException()

        current_user_id = await super().add(data)
        return str(current_user_id)



