from tests.unit.utils.login_data import password, username

login_data = [
    {"credentials": username, "password": password, "expected_status": 200},
]

logout_data = [
    {"expected_message": "You have successfully logged out.", "expected_status": 200},
]
