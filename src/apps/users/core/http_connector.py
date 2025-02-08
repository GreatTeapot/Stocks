
from typing import Optional

from httpx import AsyncClient, AsyncHTTPTransport, Limits, Timeout

from core.config import settings


class ExternalServiceConnector:
    """Class for initializing/closing and retrieving the client."""

    client: Optional[AsyncClient] = None

    @classmethod
    def start_client(cls) -> None:
        """Initialize the client at application startup."""
        transport = AsyncHTTPTransport(
            limits=Limits(
                max_connections=settings.client.max_connections,
                max_keepalive_connections=settings.client.max_keepalive_connections,
                keepalive_expiry=settings.client.keepalive_expiry,
            )
        )
        cls.client = AsyncClient(
            transport=transport, timeout=Timeout(settings.client.timeout)
        )

    @classmethod
    async def close_client(cls) -> None:
        """Close the client at application shutdown."""
        await cls.client.aclose()
        cls.client = None

    @classmethod
    def get_client(cls) -> AsyncClient:
        """Retrieve the current client."""
        if cls.client is None:
            raise RuntimeError(
                "HTTP client is not initialized. Call start_client() first."
            )
        return cls.client