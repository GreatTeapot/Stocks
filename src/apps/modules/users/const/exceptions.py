
# -------------------------- USER RESPONSES --------------------------
USER_NOT_FOUND = "User not found."
EMAIL_CONFLICT = "This email already exists."
USERNAME_CONFLICT = "This username already exists."
CREDENTIALS_CONFLICT = "Failed to verify credentials"

# -------------------------- DATA RESPONSES --------------------------
DATA_NOT_FOUND_MESSAGE = "Data not found"

# -------------------------- ERROR RESPONSES --------------------------
ADMIN_ROLE_REQUIRED_MESSAGE = "The action requires the 'admin' role."
SERVER_ERROR_MESSAGE = "Server error"
INVALID_DATA_MESSAGE = "Invalid data."
UNAUTHORIZED_USER_MESSAGE = "Unauthorized user."
NO_ACCESS_RIGHTS_MESSAGE = "No access rights."
# -------------------------- BAD REQUEST RESPONSES --------------------------
CREDENTIALS_BAD_REQUEST = "Invalid username/email or password."
USER_REMOVED_REQUEST = "User has been removed."
TOKEN_BAD_REQUEST = "Invalid token."
USER_BAD_REQUEST = "Failed to get user details."
# -------------------------- FORBIDDEN RESPONSES --------------------------
TOKEN_EXPIRED_FORBIDDEN = (
    "Your token has expired. Please log in again."
)
TOKEN_INVALID_FORBIDDEN = (
    "Error decrypting the token. Please check your request."
)
TOKEN_REQUIRED_FIELD_FORBIDDEN = (
    "Your token is missing a required field. Please contact the administrator."
)
ROLES_FORBIDDEN = "This action requires one of the roles: ..."

