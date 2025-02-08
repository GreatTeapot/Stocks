
import json
import logging
from types import TracebackType
from typing import Optional, Self, TypeVar

from fastapi import HTTPException

from common.interfaces.abstraction_uow import IUnitOfWork
from common.repositories.base import BaseRepository
from core.database import async_session_maker

TRepository = TypeVar("TRepository", bound=BaseRepository)


class BaseUnitOfWork(IUnitOfWork):
    """Base class for transaction management."""

    repo: Optional[TRepository]

    def __init__(self) -> None:
        self.__session_factory = async_session_maker

    async def __aenter__(self) -> Self:
        """Base method for entering the context manager."""
        self._session = self.__session_factory()
        return self

    async def __aexit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        """Base method for exiting the context manager."""

        # Log and raise all custom exceptions.
        if exc_type is not None and exc_type.__base__ == HTTPException:
            await self.rollback()
            logging.exception(
                json.dumps(
                    obj={
                        "exception": exc_val.__class__.__name__,
                        "status_code": getattr(exc_val, "status_code"),
                        "detail": getattr(exc_val, "detail"),
                    },
                    ensure_ascii=False,
                    indent=4,
                )
            )
            await self.close()
            raise exc_val

        # Log and raise untracked exceptions.
        if exc_type:
            await self.rollback()
            detail_massage = (
                getattr(exc_val, "detail")
                if getattr(exc_val, "detail", None)
                else exc_val.args[0] if exc_val.args else None
            )
            logging.error(
                json.dumps(
                    obj={
                        "exception": exc_val.__class__.__name__,
                        "status_code": 500,
                        "detail": detail_massage,
                    },
                    ensure_ascii=False,
                    indent=4,
                )
            )
            await self.close()
            raise HTTPException(status_code=500, detail=detail_massage)

    async def commit(self) -> None:
        """Base method for committing the transaction."""
        await self._session.commit()

    async def rollback(self) -> None:
        """Base method for rolling back the transaction."""
        await self._session.rollback()

    async def close(self) -> None:
        """Base method for closing the transaction."""
        await self._session.close()