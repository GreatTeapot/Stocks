from datetime import datetime
from types import NoneType
from typing import Optional, TypeAlias, Union
from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.orm import joinedload

from common.enums.role import UserRoleEnum
from common.repositories.mixins import PaginatedPageRepository
from common.schemas.filters.mixins import DataRangeBaseFilterSchema
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

    def __get_stmt_for_method_list(self) -> sa.Select:
        """Get the query for the list method."""
        stmt = (
            sa.select(self.model)
            .where(self.model.deleted.__eq__(False))
        )
        return stmt

    def __is_there_search_string(
        self, stmt: sa.Select, filters: DataRangeBaseFilterSchema
    ) -> sa.Select:
        """Check for the existence of a search string."""
        if filters.search_string:
            stmt = stmt.filter(
                sa.or_(
                    self.model.username.ilike(f"%{filters.search_string}"),
                    self.model.email.ilike(f"%{filters.search_string}"),
                    sa.cast(self.model.role, sa.String).ilike(f"%{filters.search_string}%"),
                ))
        return stmt

    async def get_all(
        self, filters: DataRangeBaseFilterSchema) \
            -> tuple[int, Optional[sa.ScalarResult]]:
        """Get all users with filtering by role."""
        stmt = self.__get_stmt_for_method_list()
        stmt = self.__is_there_search_string(stmt, filters)
        stmt = self._is_there_start_and_end_date(stmt, filters)
        count_records = await self._get_count_records(stmt)
        records = await self._is_there_records(count_records, stmt, filters)
        return count_records, records

