from os import wait
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url = str

    class config:
        config = ".env"


settings = Settings()
