"""Endpoints in users router"""

from fastapi import APIRouter, Depends, status

from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from api_v1.users.schemas import UserCreate, UserOut
from core.models import User
from auth import hash_password, validate_password


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post(
    "/register",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
)
async def register_user(
    user: UserCreate,
    session: AsyncSession = Depends(db_helper.get_scoped_session),
) -> UserOut:
    hashed_password: bytes = hash_password(user.password)
    user_to_db = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
    )
    session.add(user_to_db)
    await session.commit()
    return UserOut(username=user.username, email=user.email)
