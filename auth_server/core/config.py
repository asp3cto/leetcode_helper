"""Working with .env"""

from pathlib import Path

from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).parent.parent


class Settings(BaseSettings):
    """Class for .env work in pydantic style"""

    # Postgres settings that are applied if not specified in .env.auth
    postgres_password: str
    db_url: str = ""
    db_echo: bool = False

    # JWT settings that are applied if not specified in .env.auth
    secret: str = "Den Pidoras"
    private_key_path: Path = BASE_DIR / "auth" / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "auth" / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 10
    # pg: PostgresSettings = PostgresSettings()
    # jwt: JWTSettings = JWTSettings()


settings: Settings = Settings()
# create postgres url based on password from environment
settings.db_url = (
    f"postgresql+asyncpg://auth:{settings.postgres_password}@postgres/auth"
)
# NOTE: DISABLE IN PROD
settings.db_echo = True
