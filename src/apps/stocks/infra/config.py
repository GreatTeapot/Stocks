from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class CommonSettings(BaseSettings):
    """Common application settings."""


    env_file: str = (
        ".env"
    )
    env_local_file: str = (
        ".env.local"
    )

    model_config = SettingsConfigDict(
        env_file=env_local_file if env_local_file else env_file,
        env_file_encoding="utf-8",
        extra="allow",
    )

class MongoDatabase(CommonSettings):
    """Mongo database settings"""
    mongodb_connection_uri: str = Field(alias='MONGO_DB_CONNECTION_URI')
    mongodb_chat_database: str = Field(default='chat', alias='MONGODB_CHAT_DATABASE')
    mongodb_chat_collection: str = Field(default='chat', alias='MONGODB_CHAT_COLLECTION')


class Settings(CommonSettings):
    """Main application settings"""
    db : MongoDatabase = MongoDatabase()



@lru_cache
def get_settings() -> Settings:
    """
    Returns the environment settings. This function is cached and executed only once at project startup.
    """
    return Settings()


settings = get_settings()