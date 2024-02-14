"""Module with CRUD for users table in Postgres"""

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import User


async def check_user_by_username(
    session: AsyncSession,
    username: str,
) -> bool:
    statement = select(User.id).where(User.username == username)
    answer_from_db: Result = await session.execute(statement=statement)
    user = answer_from_db.scalar()
    return True if user else False


async def get_user_by_username(
    session: AsyncSession,
    username: str,
) -> User | None:
    statement = select(User).where(User.username == username)
    answer_from_db: Result = await session.execute(statement=statement)
    user = answer_from_db.scalar()
    return user


async def create_user(
    session: AsyncSession,
    username: str,
    email: str,
    hashed_password: str,
) -> None:
    user_to_db: User = User(
        username=username,
        email=email,
        hashed_password=hashed_password,
    )
    session.add(user_to_db)
    await session.commit()
    return user_to_db


async def get_user_by_id(
    session: AsyncSession,
    user_id: int,
) -> User | None:
    return await session.get(User, user_id)
