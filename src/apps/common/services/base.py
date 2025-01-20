from typing import Optional, TypeVar
from uuid import UUID

from common.interfaces.abstraction_service import IService
from common.models.base import Base
from common.schemas.filters.mixins import BaseFilterSchema
from common.schemas.pages.mixins import PageViewSchema
from common.unit_of_works.base import BaseUnitOfWork

TModel = TypeVar("TModel", bound=Base)
TDict = TypeVar("TDict", bound=dict)
TFilter = TypeVar("TFilter", bound=BaseFilterSchema)
TUnitOfWork = TypeVar("TUnitOfWork", bound=BaseUnitOfWork)
TID = TypeVar("TID", int, UUID)


class BaseService(IService):
    """Base service class."""

    @classmethod
    async def add(cls, uow: TUnitOfWork, obj_dict: TDict) -> TID:
        """Base service method for adding data."""
        async with uow:
            obj_id = await uow.repo.add(obj_dict)
            await uow.commit()
            return obj_id

    @classmethod
    async def get(cls, uow: TUnitOfWork, obj_id: TID) -> Optional[TModel]:
        """Base service method for retrieving data."""
        async with uow:
            obj = await uow.repo.get(obj_id)
            return obj

    @classmethod
    async def get_all(
        cls,
        uow: TUnitOfWork,
        filters: Optional[TFilter],
    ) -> PageViewSchema:
        """Base service method for retrieving a list of data."""

    @classmethod
    async def delete(cls, uow: TUnitOfWork, obj_id: TID) -> Optional[TID]:
        """Base service method for updating the status of data to 'deleted'."""
        async with uow:
            result = await uow.repo.delete(obj_id)
            await uow.commit()
            return result

    @classmethod
    async def delete_db(cls, uow: TUnitOfWork, obj_id: TID) -> bool:
        """Base service method for deleting data from the database."""
        async with uow:
            result = await uow.repo.delete_db(obj_id)
            await uow.commit()
            return result

    @classmethod
    async def edit(cls, uow: TUnitOfWork, obj_dict: TDict, data_id: TID) -> bool:
        """Base service method for editing data."""
        async with uow:
            result = await uow.repo.edit(obj_dict, data_id)
            await uow.commit()
            return bool(result)

    @classmethod
    async def exist(cls, uow: TUnitOfWork, obj_id: TID) -> bool:
        """Base service method for searching data."""
        async with uow:
            result = await uow.repo.exist(obj_id)
            return result