"""Working with .env"""

# NOTE: add all settings to .env

from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Class for .env work in pydantic style"""

    validate_token_endpoint: str = "http://auth_server:8000/validate/"
    mongodb_password: str
    db_url: str = ""


settings: Settings = Settings()
# create postgres url based on password from environment
settings.db_url = (
    f"mongodb://problems:{settings.mongodb_password}@mongo:27017/problems?authSource=admin"
)
print(settings.db_url)