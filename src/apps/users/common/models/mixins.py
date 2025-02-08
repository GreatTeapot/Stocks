
import uuid
from datetime import datetime

import sqlalchemy as sa
from sqlalchemy import UUID
from sqlalchemy.orm import Mapped, mapped_column


class UUIDMixin:
    """Common model for overriding the id field of type integer with a uuid4 field."""

    id: Mapped[UUID] = mapped_column(
        UUID,
        default=uuid.uuid4,
        primary_key=True,
        unique=True,
    )


class CreatedUpdatedMixin:
    """Common model for specifying creation and update timestamps."""

    created_at: Mapped[datetime] = mapped_column(sa.DateTime, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(sa.DateTime, nullable=False)