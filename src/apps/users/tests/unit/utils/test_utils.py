

def validate_response_data(response, expected_status: int, expected_data: dict = None):
    """General function to validate response status and optional response data."""
    assert response.status_code == expected_status, (
        f"Expected status {expected_status}, but got {response.status_code}. "
        f"Response content: {response.text if response.content else 'No content'}"
    )
    if expected_data:
        response_data = response.json()
        for key, value in expected_data.items():
            assert response_data.get(key) == value, f"Expected {key}={value}, got {response_data.get(key)}"
