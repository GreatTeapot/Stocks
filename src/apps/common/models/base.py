import re
from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase, declared_attr

constraint_naming_conventions = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


class BaseDeclarative(DeclarativeBase):
    """Base SQLAlchemy model."""

    metadata = MetaData(naming_convention=constraint_naming_conventions)


class Base(BaseDeclarative):
    """Base model."""

    __abstract__ = True

    pattern = re.compile(r"(?<!^)(?=[A-Z])")

    @declared_attr
    def __tablename__(cls) -> str:
        """
        Dynamic attribute for creating a table name in PostgreSQL.
        
        Example:
            class User -> "user";
        """
        return cls.pattern.sub("_", cls.__name__).lower()