"""User model for ORM"""

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

from core.models.base import Base


class User(Base):
    """User Model implementation"""

    username: Mapped[str] = mapped_column(String(15))
    hashed_password: Mapped[str] = mapped_column(String(1024))
