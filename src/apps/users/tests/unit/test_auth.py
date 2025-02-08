import pytest
from httpx import AsyncClient

from tests.unit.data.auth_data import login_data
from tests.unit.utils.test_utils import validate_response_data


@pytest.mark.asyncio
@pytest.mark.parametrize("case", login_data)
async def test_login(ac: AsyncClient, case):
    response = await ac.post("/api/v1/auth/login", json={"credentials": case["credentials"], "password": case["password"]})
    validate_response_data(response, case["expected_status"])
