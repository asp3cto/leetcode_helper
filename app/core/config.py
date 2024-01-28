"""Working with .env"""

from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).parent.parent


class JWTSettings(BaseModel):
    jwt_secret: str = "Den Pidoras"
    private_key_path: Path = BASE_DIR / "auth" / "certs" / "jwt_private.pem"
    public_key_path: Path = BASE_DIR / "auth" / "certs" / "jwt_public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 3


class PostgresSettings(BaseModel):
    db_url: str = "postgresql+asyncpg://leetcode_helper:qwerty@postgres/leetcode_helper"
    db_echo: bool = False


class Settings(BaseSettings):
    """Class for .env work in pydantic style"""

    pg: PostgresSettings = PostgresSettings()
    jwt: JWTSettings = JWTSettings()


settings: Settings = Settings()
# DISABLE IN PROD
settings.pg.db_echo = True
