"""Module with pydantic schemas for views.py"""

from typing import Annotated
from annotated_types import MinLen, MaxLen
from pydantic import BaseModel


class CreateUser(BaseModel):
    """Model for user creation"""

    username: Annotated[str, MinLen(6), MaxLen(15)]
