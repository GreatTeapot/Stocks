
import os

from functools import lru_cache
from pathlib import Path
from typing import Optional, Self

from pydantic import Field, HttpUrl, PostgresDsn, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL


class CommonSettings(BaseSettings):
    """Common application settings."""

    model_config = SettingsConfigDict(
        env_file=os.path.expanduser(".env"),
        env_file_encoding="utf-8",
        extra="allow",
    )



class HttpxSettings(CommonSettings):
    """Environment settings for working with the HTTP client."""

    max_connections: int = Field(default=500, alias="MAX_CONNECTIONS")
    max_keepalive_connections: int = Field(default=50, alias="MAX_KEEPALIVE_CONNECTIONS")
    keepalive_expiry: float = Field(default=30.0, alias="KEEPALIVE_EXPIRY")
    timeout: float = Field(default=20.0, alias="TIMEOUT")



class AuthSettings(CommonSettings):
    """Environment settings for connecting to the Auth service"""

    token_url: HttpUrl = Field(
        default="http://localhost:8000/api/v1/auth/login", alias="TOKEN_URL")

    private_key_path: Path = Field(
        default="certs/jwt-private.pem", alias="PRIVATE_KEY_PATH"
    )
    public_key_path: Path = Field(default="certs/jwt-public.pem", alias="PUBLIC_KEY_PATH")
    algorithm: str = Field(default="RS256", alias="ALGORITHM")
    access_token_expire_minutes: int = Field(
        default=60, alias="ACCESS_TOKEN_EXPIRE_MINUTES"
    )
    refresh_token_expire_minutes: int = Field(
        default=10000, alias="REFRESH_TOKEN_EXPIRE_MINUTES"
    )


class AuthorizationService(CommonSettings):
    """Connection for other authorization services"""
    # Google
    secret_key: str = Field(default="secret", alias="SECRET_KEY")
    GOOGLE_CLIENT_ID: int = Field(default=0, alias="GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET: str = Field(default="GOOGLE_CLIENT_SECRET", alias="GOOGLE_CLIENT_SECRET")
    GOOGLE_REDIRECT_URI: str = Field(default="http://localhost:8000/api/v1/auth/google/callback" ,
                                     alias="GOOGLE_REDIRECT_URI")
    GOOGLE_SERVER_METADATA_URL: str = Field(default="https://accounts.google.com/.well-known/openid-configuration",
                                           alias="GOOGLE_SERVER_METADATA_URL")

class DatabaseSettings(CommonSettings):
    """Database environment settings."""

    pg_host: str = Field(default="localhost", alias="PG_HOST")
    pg_user: str = Field(default="postgres", alias="PG_USER")

    pg_password: str = Field(default="postgres", alias="PG_PASSWORD")
    pg_database: str = Field(default="stocks", alias="PG_DATABASE",)
    pg_port: int = Field(default=5432, alias="PG_PORT")
    async_database_url: Optional[PostgresDsn] = Field(default=None)
    sync_database_url: Optional[PostgresDsn] = Field(default=None)

    @staticmethod
    def __build_db_dsn(
        username: str,
        password: str,
        host: str,
        port: int,
        database: str,
        async_dsn: bool = False,
    ) -> URL:
        """Factory for PostgreSQL DSN."""
        driver_name = "postgresql"
        if async_dsn:
            driver_name += "+asyncpg"
        return URL.create(
            drivername=driver_name,
            username=username,
            password=password,
            host=host,
            port=port,
            database=database,
        )

    @model_validator(mode="after")
    def validate_async_database_url(self) -> Self:
        """Build asynchronous PostgreSQL DSN."""
        self.async_database_url = self.__build_db_dsn(
            username=self.pg_user,
            password=self.pg_password,
            host=self.pg_host,
            port=self.pg_port,
            database=self.pg_database,
            async_dsn=True,
        )
        return self

    @model_validator(mode="after")
    def validate_sync_database_url(self) -> Self:
        """Build synchronous PostgreSQL DSN."""
        self.sync_database_url = self.__build_db_dsn(
            username=self.pg_user,
            password=self.pg_password,
            host=self.pg_host,
            port=self.pg_port,
            database=self.pg_database,
        )
        return self



class Settings(CommonSettings):
    """Environment settings."""

    db: DatabaseSettings = DatabaseSettings()
    auth: AuthSettings = AuthSettings()
    client: HttpxSettings = HttpxSettings()
    authorization: AuthorizationService = AuthorizationService()

    client_id: str = Field(default="fastapi", alias="CLIENT_ID")
    client_secret: str = Field(default="fastapi_secret", alias="CLIENT_SECRET")

    port: int = Field(default=8000, alias="PORT")
    host: str = Field(alias="HOST")
    default_page_size: int = Field(default=30, alias="PAGE_SIZE")
    max_page_size: int = Field(default=30, alias="MAX_PAGE_SIZE")
    openapi_url: str = Field(default="/docs", alias="OPENAPI_URL")


@lru_cache
def get_settings() -> Settings:
    """
    Returns the environment settings. This function is cached and executed only once at project startup.
    """
    return Settings()


settings = get_settings()

