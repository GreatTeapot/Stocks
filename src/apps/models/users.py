
from typing import Optional

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from common.enums.role import UserRoleEnum
from common.models.base import Base
from common.models.mixins import CreatedUpdatedMixin, UUIDMixin


class User(Base, CreatedUpdatedMixin, UUIDMixin):
    """User model"""

    username: Mapped[Optional[str]] = mapped_column(sa.String(length=100))
    last_name: Mapped[Optional[str]] = mapped_column(sa.String(length=100), nullable=True)
    first_name: Mapped[Optional[str]] = mapped_column(sa.String(length=100), nullable=True)
    photo: Mapped[Optional[str]] = mapped_column(sa.String(length=100), nullable=True)
    email: Mapped[Optional[str]] = mapped_column(
        sa.String(length=250), index=True, unique=True
    )
    password_hash: Mapped[Optional[bytes]] = mapped_column(sa.LargeBinary, nullable=False)
    role: Mapped[UserRoleEnum] = mapped_column(
        sa.Enum(UserRoleEnum, name="user_roles"),
        default=UserRoleEnum.USER,
        nullable=False,
    )
    logged_out: Mapped[bool] = mapped_column(sa.Boolean, default=False, nullable=False)
    deleted: Mapped[bool] = mapped_column(sa.Boolean, default=False, nullable=False)
    is_active: Mapped[bool] = mapped_column(sa.Boolean, default=False, nullable=False)
