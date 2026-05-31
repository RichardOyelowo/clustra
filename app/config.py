from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    database_url: str = Field(default=...)
    test_database_url: str = Field(default=...)
    secret_key: str = Field(default=...)
    acesss_token_expiry: int = Field(default=...)
    refresh_token_exppiry: int =Field(default=...)


settings = Settings()
