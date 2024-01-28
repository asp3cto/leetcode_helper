"""Endpoints in users router"""

from fastapi import APIRouter, Depends, status, HTTPException, Form

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import pg_db_helper
from api_v1.users.schemas import UserIn, UserOut
from core.models import User
from auth import hash_password, validate_password


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post(
    "/register/",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
)
async def register_user(
    user: UserIn,
    session: AsyncSession = Depends(pg_db_helper.get_scoped_session),
) -> UserOut:
    # check if user already in db
    statement = select(User).where(User.username == user.username)
    answer_from_db = await session.execute(statement=statement)
    if answer_from_db.first():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="User already exists"
        )

    hashed_password: bytes = hash_password(user.password)
    user_to_db: User = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
    )
    session.add(user_to_db)
    await session.commit()
    return UserOut(username=user.username, email=user.email)


@router.post(
    "/login/",
    status_code=status.HTTP_302_FOUND,
)
async def login_user(
    username: str = Form(),
    password: str = Form(),
    session: AsyncSession = Depends(pg_db_helper.get_scoped_session),
) -> dict:
    invalid_login_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password",
    )

    statement = select(User.hashed_password).where(User.username == username)
    answer_from_db = (await session.execute(statement=statement)).first()

    if not answer_from_db:
        raise invalid_login_exception

    hash_from_db: bytes = answer_from_db[0]
    if validate_password(password, hash_from_db):
        return {"detail": "Authorized"}
    raise invalid_login_exception
