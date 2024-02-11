"""Endpoints in users router"""

from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    status,
    HTTPException,
    Response,
    Cookie,
)

from sqlalchemy.ext.asyncio import AsyncSession

from core.models import User
from core.models import pg_db_helper
from api_v1.users.schemas import UserIn, UserOut, TokenInfo
from auth import (
    hash_password,
    encode_jwt,
    encode_refresh_jwt,
)
from api_v1.users.crud import check_user_by_username, create_user
from api_v1.users.dependencies import (
    validate_auth_user_password,
    validate_tokens,
    get_current_auth_user,
)


router = APIRouter(
    tags=["Users"],
)


@router.get("/")
def home():
    return {"detail": "home"}


@router.post(
    "/register/",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
)
async def register_user(
    response: Response,
    user: UserIn,
    session: AsyncSession = Depends(pg_db_helper.scoped_session_dependency),
    access_token: Annotated[str | None, Cookie()] = None,
    refresh_token: Annotated[str | None, Cookie()] = None,
) -> UserOut:
    # removing access_token cookie
    headers = {}
    if refresh_token:
        response.delete_cookie("refresh_token")
    if access_token:
        response.delete_cookie("access_token")
    if refresh_token or access_token:
        headers = {"set-cookie": response.headers["set-cookie"]}
    # check if user already in db
    if await check_user_by_username(session=session, username=user.username):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User already exists",
            headers=headers,
        )
    hashed_password: bytes = hash_password(user.password)
    await create_user(session, user.username, user.email, hashed_password)
    return UserOut(username=user.username, email=user.email)


@router.post("/login/", status_code=status.HTTP_200_OK, response_model=TokenInfo)
async def login_user(
    response: Response,
    user: User = Depends(validate_auth_user_password),
) -> TokenInfo:
    # create token and put it to cookie
    access_token_value = encode_jwt(
        payload={"sub": user.id},
    )
    response.set_cookie(
        key="access_token",
        value=f"{access_token_value}",
        httponly=True,
        samesite="lax",
    )
    refresh_token_value = encode_refresh_jwt(
        payload={"sub": user.id},
    )
    response.set_cookie(
        key="refresh_token",
        value=f"{refresh_token_value}",
        httponly=True,
        samesite="lax",
    )
    return TokenInfo(
        access_token=access_token_value,
        refresh_token=refresh_token_value,
        token_type="Bearer",
    )


@router.post("/logout/")
async def logout_user(
    response: Response,
    access_token: Annotated[str | None, Cookie()] = None,
    refresh_token: Annotated[str | None, Cookie()] = None,
):
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="User isnt logged in"
        )
    response.delete_cookie("access_token")
    if refresh_token:
        response.delete_cookie("refresh_token")
    return {"detail": "Logged out"}


@router.get("/validate/")
async def validate_token(
    refresh_payload=Depends(validate_tokens),
    user: User = Depends(get_current_auth_user),
):
    return {
        "username": user.username,
        "email": user.email,
        "exp": refresh_payload["exp"],
    }
