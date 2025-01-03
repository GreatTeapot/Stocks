from sqlalchemy import or_, select

from common.repositories.mixins import PaginatedPageRepository
from models import User


class AuthRepository(PaginatedPageRepository):
    """Repository for user-specific operations."""

    model = User

    async def get_by_email_or_username(
        self, email: str, username: str
    ) :
        """
        Retrieve a user by email or username.

        :param email: Email to filter.
        :param username: Username to filter.
        :return: User instance if found, None otherwise.
        """
        stmt = (
            select(self.model)
            .filter(
                or_(
                    self.model.email == email,
                    self.model.username == username,
                ),
                self.model.deleted.__eq__(False),
            )
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()
