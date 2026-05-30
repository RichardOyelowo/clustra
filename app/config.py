from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    database_url: str = Field(default=...)
    test_database_url: str = Field(default=...)
    secret_key: str = Field(default=...)
    acesss_token_expiry: int = Field(default=...)
    refresh_token_exppiry: int =Field(default=...)

    class Config:
        env_file = ".env"


settings = Settings()
