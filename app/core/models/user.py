"""User model for ORM"""

from typing import AsyncGenerator
from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .base import Base
from .helper import db_helper


class User(Base, SQLAlchemyBaseUserTable[int]):
    pass


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with db_helper.session_factory() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)
