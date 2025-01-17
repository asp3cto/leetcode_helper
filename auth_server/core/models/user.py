"""Module with User model for db"""

from sqlalchemy import String, LargeBinary, sql
from sqlalchemy.orm import Mapped, mapped_column

from core.models import Base


class User(Base):
    """User model for db"""

    username: Mapped[str] = mapped_column(String(30), unique=True)
    email: Mapped[str | None]
    is_active: Mapped[bool] = mapped_column(server_default=sql.true())
    hashed_password: Mapped[bytes] = mapped_column(LargeBinary())
