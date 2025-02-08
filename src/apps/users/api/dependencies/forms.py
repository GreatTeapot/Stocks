from fastapi.security import OAuth2PasswordRequestForm
from pydantic import Field

class CustomOAuth2PasswordRequestForm(OAuth2PasswordRequestForm):
    credentials: str = Field(..., alias="username")
    password: str = Field(...)

    class Config:
        allow_population_by_field_name = True
