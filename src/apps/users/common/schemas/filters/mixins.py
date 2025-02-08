from datetime import datetime
from math import ceil
from typing import Optional, TypeVar

from pydantic import Field

from common.schemas.base import BaseModel
from core.config import settings

TSchema = TypeVar("TSchema", bound=BaseModel)


class BaseFilterSchema(BaseModel):
    """Base filter schema."""

    page_number: int = Field(ge=1, description="Page number", default=1)
    page_size: int = Field(
        ge=1, le=settings.max_page_size, default=settings.default_page_size, description="Page size"
    )
    search_string: Optional[str] = Field(default=None, description="Search string")


    

class DataRangeBaseFilterSchema(BaseFilterSchema):
    """Schema for the base data range filter."""

    date_begin: Optional[datetime] = Field(default=None)
    date_end: Optional[datetime] = Field(default=None)