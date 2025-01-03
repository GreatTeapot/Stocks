from typing import Optional, TypeVar

import sqlalchemy as sa
from sqlalchemy import ScalarResult, Select

from common.models.base import Base
from common.repositories.base import BaseRepository
from common.schemas.filters.mixins import BaseFilterSchema, DataRangeBaseFilterSchema

TModel = TypeVar("TModel", bound=Base)
TFilter = TypeVar("TFilter", bound=BaseFilterSchema)
TFilterData = TypeVar("TFilterData", bound=DataRangeBaseFilterSchema)


class PaginatedPageRepository(BaseRepository):
    """General repository for splitting data into pages."""

    model: type[TModel]

    def _is_there_start_and_end_date(self, stmt: Select, filters: TFilterData) -> Select:
        """Check for the existence of start and end dates."""
        if filters.date_begin:
            stmt = stmt.filter(self.model.updated_at >= filters.date_begin.date())
        if filters.date_end:
            stmt = stmt.filter(self.model.updated_at <= filters.date_end.date())
        return stmt

    async def _get_count_records(self, stmt: Select) -> int:
        """Get the number of records."""
        # Create a subquery from the given `stmt` expression.
        subquery = stmt.subquery()

        # Use `func.count` to count records in the subquery.
        count_records = (
            await self.session.execute(
                sa.select(sa.func.count().label("count")).select_from(subquery)
            )
        ).scalar_one()
        return count_records

    async def _is_there_records(
        self, count_records: int, stmt: Select, filters: TFilter
    ) -> Optional[ScalarResult]:
        """Check for the existence of a record."""
        if count_records != 0:
            total_pages = (count_records - 1) // filters.page_size

            # Set page_number to the last page if the requested page
            # exceeds the number of available pages.
            page_number = min(filters.page_number, total_pages)
            records = (
                await self.session.execute(
                    stmt.order_by(self.model.updated_at.desc())
                    .offset(page_number * filters.page_size)
                    .limit(filters.page_size)
                )
            ).scalars()
            return records