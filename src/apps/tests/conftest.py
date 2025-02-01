import asyncio

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport

from common.models.base import Base
from core.config import settings
from core.database import engine_async
from main import app
from tests.utils import get_base_url


@pytest_asyncio.fixture(scope='session', autouse=True)
async def prepare_database():
    if not settings.db.pytest_debug:
        pytest.exit("PYTEST_DEBUG is not set to True, skipping tests.")

    async with engine_async.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield None
    async with engine_async.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="session")
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def ac() -> AsyncClient:
    async with AsyncClient(transport=ASGITransport(app=app), base_url=get_base_url()) as async_test_client:
        yield async_test_client

