"""Working with .env"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Class for .env work in pydantic style"""

    db_url: str = "postgresql+asyncpg://root:root@127.0.0.1:5555/leetcode_helper"
    db_echo: bool = False


settings: Settings = Settings()
# DISABLE IN PROD
settings.db_echo = True
