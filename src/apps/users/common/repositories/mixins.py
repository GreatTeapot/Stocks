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
            # Total pages as one-based index
            total_pages = (count_records + filters.page_size - 1) // filters.page_size

            # Clamp page_number to valid range (1 to total_pages)
            page_number = max(1, min(filters.page_number, total_pages))

            # Calculate offset based on zero-based index
            offset = (page_number - 1) * filters.page_size

            records = (
                await self.session.execute(
                    stmt.order_by(self.model.updated_at.desc())
                    .offset(offset)
                    .limit(filters.page_size)
                )
            ).scalars()
            return records