import abc
from typing import Any, Optional, TypeVar
from uuid import UUID

from common.models.base import Base
from common.schemas.filters.mixins import BaseFilterSchema
from common.schemas.pages.mixins import PageViewSchema
from common.unit_of_works.base import BaseUnitOfWork

TModel = TypeVar("TModel", bound=Base)
TDict = TypeVar("TDict", bound=dict)
TFilter = TypeVar("TFilter", bound=BaseFilterSchema)
TUnitOfWork = TypeVar("TUnitOfWork", bound=BaseUnitOfWork)
TID = TypeVar("TID", int, UUID)


class IService(abc.ABC):
    """Abstract service class."""

    @classmethod
    @abc.abstractmethod
    async def add(cls, uow: TUnitOfWork, obj_dict: TDict) -> Any:
        """Abstract service method for adding data."""

    @classmethod
    @abc.abstractmethod
    async def get(cls, uow: TUnitOfWork, obj_id: TID) -> Optional[TModel]:
        """Abstract service method for retrieving data."""

    @classmethod
    @abc.abstractmethod
    async def get_all(
        cls, uow: TUnitOfWork, filters: Optional[TFilter]
    ) -> PageViewSchema:
        """Abstract service method for retrieving a list of data."""

    @classmethod
    @abc.abstractmethod
    async def delete(cls, uow: TUnitOfWork, obj_id: TID) -> Optional[TID]:
        """Abstract service method for updating data status to 'deleted'."""

    @classmethod
    @abc.abstractmethod
    async def delete_db(cls, uow: TUnitOfWork, obj_id: TID) -> bool:
        """Abstract service method for deleting data from the database."""

    @classmethod
    @abc.abstractmethod
    async def edit(cls, uow: TUnitOfWork, obj_dict: TDict, data_id: TID) -> bool:
        """Abstract service method for editing data."""

    @classmethod
    @abc.abstractmethod
    async def exist(cls, uow: TUnitOfWork, obj_id: TID) -> bool:
        """Abstract service method for searching for data."""