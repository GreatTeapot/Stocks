from httpx import AsyncClient

async def get_access_token(ac: AsyncClient, username: str, password: str) -> str:
    """function to get access token from login controller"""
    response = await ac.post("/api/v1/auth/login", json={"credentials": username, "password": password})
    assert response.status_code == 200, "Login failed"
    return response.json().get("access_token")
