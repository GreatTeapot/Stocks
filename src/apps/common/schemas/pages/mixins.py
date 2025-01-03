from typing import Generic, TypeVar

from pydantic import Field

from common.schemas.base import BaseModel

TSchema = TypeVar("TSchema", bound=BaseModel)


class PageSchema(BaseModel, Generic[TSchema]):
    """Page schema."""

    count_records: int = Field(ge=0, default=0)
    records: list[TSchema]


class PageViewSchema(PageSchema[TSchema]):
    """Page representation schema."""

    page: int = Field(ge=0, default=0)
    max_page_count: int