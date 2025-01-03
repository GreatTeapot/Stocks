from datetime import datetime
from math import ceil
from typing import Optional, TypeVar

from pydantic import Field

from common.schemas.base import BaseModel
from core.config import settings

TSchema = TypeVar("TSchema", bound=BaseModel)


class BaseFilterSchema(BaseModel):
    """Base filter schema."""

    page_number: int = Field(ge=1, description="Page number")
    page_size: int = Field(
        ge=1, le=30, default=settings.page_size, description="Page size"
    )
    total_objects: Optional[int] = Field(default=None, description="Total number of objects available")
    search_string: Optional[str] = Field(default=None, description="Search string")


    

class DataRangeBaseFilterSchema(BaseFilterSchema):
    """Schema for the base data range filter."""

    date_begin: Optional[datetime] = Field(default=None)
    date_end: Optional[datetime] = Field(default=None)