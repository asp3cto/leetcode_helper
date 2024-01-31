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
from fastapi.security import OAuth2PasswordRequestForm
from jwt import InvalidTokenError, ExpiredSignatureError

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import User
from core.models import pg_db_helper
from api_v1.users.schemas import UserIn, UserOut, TokenInfo
from auth import (
    hash_password,
    validate_password,
    encode_jwt,
    decode_jwt,
    encode_refresh_jwt,
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
    session: AsyncSession = Depends(pg_db_helper.get_scoped_session),
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
    statement = select(User).where(User.username == user.username)
    answer_from_db = await session.execute(statement=statement)
    if answer_from_db.first():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User already exists",
            headers=headers,
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


async def validate_auth_user_password(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(pg_db_helper.get_scoped_session),
):
    """Helper Function for login route to check a user by password"""
    invalid_login_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password",
    )
    statement = select(User).where(User.username == form_data.username)
    answer_from_db = (await session.execute(statement=statement)).first()

    # if no user was found by username in db
    if not answer_from_db:
        raise invalid_login_exception

    user_from_db: User = answer_from_db[0]
    hash_from_db: bytes = user_from_db.hashed_password

    # if passwords dont match
    if not validate_password(form_data.password, hash_from_db):
        raise invalid_login_exception

    if not user_from_db.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="User is not active"
        )

    return user_from_db


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


def validate_tokens(
    response: Response,
    access_token: Annotated[str | None, Cookie()] = None,
    refresh_token: Annotated[str | None, Cookie()] = None,
) -> dict:
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="user is not logged in",
        )
    refresh_payload = {}
    try:
        refresh_payload = decode_jwt(
            token=refresh_token,
        )
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            # NOTE: REMOVE EXCEPTION IN PROD
            detail=f"invalid refresh token error: {e}",
        )
    # if we dont need to create new access_token, use old one as new :)
    new_access_token = access_token
    # if access_token is expired, generate new one
    try:
        decode_jwt(
            token=access_token,
        )
    except ExpiredSignatureError as e:
        new_access_token = encode_jwt(payload={"sub": refresh_payload["sub"]})

    # return new access token to set to cookie
    response.set_cookie("access_token", new_access_token)
    return refresh_payload


def get_current_refresh_token_payload(
    refresh_token: Annotated[str | None, Cookie()] = None,
) -> dict:
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="user is not logged in",
        )
    payload = {}
    try:
        payload = decode_jwt(
            token=refresh_token,
        )
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            # NOTE: REMOVE EXCEPTION IN PROD
            detail=f"invalid refresh token error: {e}",
        )
    return payload


async def get_current_auth_user(
    payload: dict = Depends(get_current_refresh_token_payload),
    session: AsyncSession = Depends(pg_db_helper.get_scoped_session),
) -> User:
    id: int | None = payload.get("sub")

    # check user in db
    statement = select(User).where(User.id == id)
    answer_from_db = (await session.execute(statement=statement)).first()

    # if no user was found by username in db
    if not answer_from_db:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            # NOTE: REMOVE ADDITIONAL INFO IN PROD
            detail="token invalid (user not found)",
        )

    user_from_db = answer_from_db[0]
    if user_from_db.is_active:
        return user_from_db
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="user inactive",
    )


@router.get("/validate/")
def validate_token(
    refresh_payload=Depends(validate_tokens),
    user: User = Depends(get_current_auth_user),
):
    return {
        "username": user.username,
        "email": user.email,
        "exp": refresh_payload["exp"],
    }
