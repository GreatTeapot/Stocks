from typing import Self

from common.unit_of_works.base import BaseUnitOfWork
from modules.users.repositories.auth import AuthRepository


class AuthUOW(BaseUnitOfWork):
    """Class for handling authentication transactions."""

    repo = AuthRepository

    async def __aenter__(self) -> Self:
        """Enter the context manager."""
        await super().__aenter__()
        self.repo = AuthRepository(self._session)
        return self

