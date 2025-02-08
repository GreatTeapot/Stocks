from datetime import datetime
from types import NoneType
from typing import TypeAlias, Union
from uuid import UUID

from common.enums.role import UserRoleEnum
from common.schemas.filters.mixins import DataRangeBaseFilterSchema
from common.schemas.pages.mixins import PageViewSchema
from common.services.mixins import PaginatedPageService
from core.security import Security
from models import User
from modules.users.exceptions.user import UserNotFoundException
from modules.users.schemas.user import RegisterSchema, CurrentUserSchema
from modules.users.schemas.user import UpdateUserSchema
from modules.users.unit_of_works.user import UserUOW

RegisterData: TypeAlias = dict[
    str, Union[bytes, str, datetime, bool, UserRoleEnum, NoneType, int]
]
EditData: TypeAlias = dict[str, Union[UUID, str, bool, datetime, int, None]]


class UserService(PaginatedPageService):
    """Service for working with a user profile."""
    @staticmethod
    def __add_data_for_create(user_data: RegisterData) -> RegisterData:
        """Add data for creating a new user."""
        user_data.update(password_hash=Security.hash_password(user_data["password_hash"]))
        user_data.update(is_active=True) # Turn to False when add logic for activation user(email, phone number, e.t.c)
        return user_data

    @staticmethod
    def __convert_record(record: User) -> CurrentUserSchema:
        """Convert a record into a pydantic model."""
        return CurrentUserSchema(
            id=record.id,
            username=record.username,
            first_name=record.first_name,
            last_name=record.last_name,
            email=record.email,
            role=record.role
        )

    @classmethod
    async def create(cls, uow: UserUOW, schema: RegisterSchema) -> RegisterSchema:
        """Create a new user."""
        user_data = schema.model_dump()
        user_update_data = cls.__add_data_for_create(user_data)
        result = await cls.add(uow=uow, obj_dict=user_update_data)
        return result


    @classmethod
    async def get_user(cls, uow: UserUOW, user_id: UUID) -> CurrentUserSchema:
        """Get user profile."""
        current_user = await cls.get(uow, user_id)
        if current_user is None:
            raise UserNotFoundException()
        return current_user

    @classmethod
    async def update(
        cls, uow: UserUOW, model: UpdateUserSchema, user_id: UUID
    ) -> bool:
        """Update user data."""
        user_data = model.model_dump()
        result = await cls.edit(uow=uow, obj_dict=user_data, data_id=user_id)
        return result

    @classmethod
    async def delete_user(cls, uow: UserUOW, user_id: UUID) -> bool:
        """Set user status to deleted."""
        result = await cls.delete(uow=uow, obj_id=user_id)
        return bool(result)

    @classmethod
    async def get_all(cls, uow: UserUOW, filters: DataRangeBaseFilterSchema) \
            -> PageViewSchema:
        """Get all users with filtering """
        async with uow:
            count_records, records = await uow.repo.get_all(filters)
            if records is None:
                list_records = []
            else:
                list_records = [
                    cls.__convert_record(record) for record in cls._gen_records(records)
                ]
            response = cls._get_response(
                count_records, CurrentUserSchema, list_records, filters
            )
            return response
