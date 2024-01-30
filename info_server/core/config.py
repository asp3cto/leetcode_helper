"""Working with .env"""

# NOTE: add all settings to .env

from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Class for .env work in pydantic style"""

    validate_token_endpoint: str = "http://auth_server:8000/validate/"


settings: Settings = Settings()
