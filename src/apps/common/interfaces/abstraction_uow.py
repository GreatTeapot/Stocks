import abc
from typing import TypeVar

from common.repositories.base import BaseRepository


TRepository = TypeVar("TRepository", bound=BaseRepository)

class IUnitOfWork(abc.ABC):
    """Abstract class for managing transactions."""

    @abc.abstractmethod
    def __init__(self) -> None: ...

    @abc.abstractmethod
    async def __aenter__(self) -> TRepository:
        """Abstract method for entering a context manager."""

    @abc.abstractmethod
    async def __aexit__(self, *args) -> None:
        """Abstract method for exiting a context manager."""

    @abc.abstractmethod
    async def commit(self) -> None:
        """Abstract method for committing a transaction."""

    @abc.abstractmethod
    async def rollback(self) -> None:
        """Abstract method for rolling back a transaction."""

    @abc.abstractmethod
    async def close(self) -> None:
        """Abstract method for closing a transaction."""