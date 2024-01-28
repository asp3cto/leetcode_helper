"""Working with .env"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Class for .env work in pydantic style"""

    db_url: str = "postgresql+asyncpg://leetcode_helper:qwerty@postgres/leetcode_helper"
    db_echo: bool = False
    jwt_secret: str = "Den Pidoras"


settings: Settings = Settings()
# DISABLE IN PROD
settings.db_echo = True
