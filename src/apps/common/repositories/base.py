from datetime import datetime
from typing import Optional, TypeAlias, TypeVar, Union
from uuid import UUID

from sqlalchemy import ScalarResult, delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from common.interfaces.abstraction_repository import IRepository
from common.models.base import Base
from common.schemas.base import BaseModel
from common.schemas.filters.mixins import BaseFilterSchema

TModel = TypeVar("TModel", bound=Base)
TSchema = TypeVar("TSchema", bound=BaseModel)
TFilter = TypeVar("TFilter", bound=BaseFilterSchema)

EditData: TypeAlias = dict[str, Union[UUID, str, bool, datetime, int, None]]
TID = TypeVar("TID", int, UUID)


class BaseRepository(IRepository):
    """Base repository class."""

    model: type[TModel]

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(self, data: dict) -> TID:
        """Base repository method for adding data."""
        stmt = insert(self.model).values(**data).returning(self.model.id)
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def get(self, data_id: TID) -> Optional[TModel]:
        """Base repository method for retrieving data."""
        stmt = (
            select(self.model)
            .filter(
                data_id == self.model.id,
                self.model.deleted.__eq__(False),
                )
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def get_all(self, filters: TFilter):
        """Base repository method for retrieving a list of data."""
        raise NotImplementedError()

    async def delete(self, data_id: TID) -> Optional[TID]:
        """Base repository method for updating data status to "deleted"."""
        stmt = (
            update(self.model)
            .filter(data_id == self.model.id, self.model.deleted.__eq__(False))
            .values(deleted=True, updated_at=datetime.now())
            .returning(self.model.id)
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def delete_db(self, data_id: TID) -> bool:
        """Base repository method for deleting data from the database."""
        stmt = delete(self.model).where(data_id == self.model.id).returning(self.model.id)
        res = await self.session.execute(stmt)
        return bool(res.scalar_one_or_none())

    async def edit(self, data: EditData, data_id: TID) -> Optional[UUID]:
        """Base repository method for editing data."""
        stmt = (
            update(self.model)
            .filter(data_id == self.model.id, self.model.deleted.__eq__(False))
            .values(**data)
            .returning(self.model.id)
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def exist(self, obj_id: TID) -> bool:
        """Base repository method for finding data."""
        stmt = select(self.model).filter(
            obj_id == self.model.id, self.model.deleted.__eq__(False)
        )
        res = await self.session.execute(stmt)
        return bool(res.scalar_one_or_none())