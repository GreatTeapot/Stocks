from tests.unit.data.auth_data import username, password


register_data = [
    {
        "username": username,
        "email": "test@gmail.com",
        "password_hash": password,
        "expected_status": 200,

    },
    {
        "username": "us#@",  # Invalid username
        "email": "invalid_email@example.com",
        "password_hash": "123",
        "expected_status": 422,
    },
]
profile_data = [
    {
        "expected_status": 200,
    },
]
