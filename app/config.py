from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str
    secret_key: str
    acesss_token_expiry: int
    refresh_token_exppiry: int

    class Config:
        env_file = ".env"


settings = Settings()
