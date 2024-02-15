"""Working with .env"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Class for .env work in pydantic style"""

    validate_token_endpoint: str = "http://auth_server:8000/validate/"
    mongodb_password: str
    db_url: str = ""
    csv_file: str = "./data/problems.csv"


settings: Settings = Settings()
# create postgres url based on password from environment
settings.db_url = f"mongodb://problems:{settings.mongodb_password}@mongo:27017/problems?authSource=admin"
