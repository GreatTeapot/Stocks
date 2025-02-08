import pytest
from httpx import AsyncClient

from tests.unit.data.user_data import register_data
from tests.unit.utils.auth_util import get_access_token
from tests.unit.utils.login_data import password, username
from tests.unit.utils.test_utils import validate_response_data


@pytest.mark.asyncio
@pytest.mark.parametrize("case", register_data)
async def test_register_user(ac: AsyncClient, case):
    response = await ac.post("/api/v1/user/register", json=case)
    validate_response_data(response, case["expected_status"])


@pytest.mark.asyncio
async def test_user_profile(ac: AsyncClient):
    access_token = await get_access_token(ac, username, password)
    headers = {"Authorization": f"Bearer {access_token}"}
    response = await ac.get("/api/v1/user/profile", headers=headers)
    validate_response_data(response, 200)


