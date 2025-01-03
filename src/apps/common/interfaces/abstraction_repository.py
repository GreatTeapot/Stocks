
from abc import ABC, abstractmethod
from datetime import datetime
from types import NoneType
from typing import Optional, TypeAlias, TypeVar, Union
from uuid import UUID

from sqlalchemy import ScalarResult

from common.enums.role import UserRoleEnum
from common.models.base import Base
from common.schemas.base import BaseModel
from common.schemas.filters.mixins import BaseFilterSchema

TModel = TypeVar("TModel", bound=Base)
TSchema = TypeVar("TSchema", bound=BaseModel)
TFilter = TypeVar("TFilter", bound=BaseFilterSchema)
TID = TypeVar("TID", int, UUID)

RegisterData: TypeAlias = dict[str, Union[str, datetime, bool, UserRoleEnum, NoneType]]
EditData: TypeAlias = dict[str, Union[UUID, str, bool, datetime, int, None]]


class IRepository(ABC):
    """Abstract repository class."""

    model: type[TModel]

    @abstractmethod
    async def add(self, data: RegisterData) -> TID:
        """Abstract repository method for adding data."""

    @abstractmethod
    async def get(self, data_id: TID) -> Optional[TModel]:
        """Abstract repository method for retrieving data."""

    @abstractmethod
    async def get_all(self, filters: TFilter) -> tuple[int, Optional[ScalarResult]]:
        """Abstract repository method for retrieving a list of data."""

    @abstractmethod
    async def delete(self, data_id: TID) -> Optional[TID]:
        """Abstract repository method for updating the data status to 'deleted'."""

    @abstractmethod
    async def delete_db(self, data_id: TID) -> bool:
        """Abstract repository method for removing data from the database."""

    @abstractmethod
    async def edit(self, data: EditData, data_id: TID) -> bool:
        """Abstract repository method for editing data."""

    @abstractmethod
    async def exist(self, obj_id: TID) -> bool:
        """Abstract repository method for checking existence of data."""