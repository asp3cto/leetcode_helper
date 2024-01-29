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
from jwt import InvalidTokenError

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import User
from core.models import pg_db_helper
from api_v1.users.schemas import UserIn, UserOut, TokenInfo
from auth import hash_password, validate_password, encode_jwt, decode_jwt
from auth import OAuth2PasswordBearerWithCookie


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="/users/login/")


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
) -> UserOut:
    # removing access_token cookie
    headers = {}
    if access_token:
        response.delete_cookie("access_token")
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
    access_token: Annotated[str | None, Cookie()] = None,
) -> TokenInfo:
    # if we got to this route while already logged in
    if access_token:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User already authorized",
        )
    # create token and put it to cookie
    access_token_value = encode_jwt(
        payload={"sub": user.id},
    )
    response.set_cookie(
        key="access_token", value=f"Bearer {access_token_value}", httponly=True
    )
    return TokenInfo(access_token=access_token_value, token_type="Bearer")


@router.post("/logout/")
async def logout_user(
    response: Response,
    access_token: Annotated[str | None, Cookie()] = None,
):
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User isnt logged in"
        )
    response.delete_cookie("access_token")
    return {
        "detail": "Logged out"
    }


def get_current_token_payload(
    token: str = Depends(oauth2_scheme),
) -> dict:
    try:
        payload = decode_jwt(
            token=token,
        )
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            # NOTE: REMOVE EXCEPTION IN PROD
            detail=f"invalid token error: {e}",
        )
    return payload


async def get_current_auth_user(
    payload: dict = Depends(get_current_token_payload),
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


@router.get("/me/")
def auth_user_check_self_info(
    payload: dict = Depends(get_current_token_payload),
    user: User = Depends(get_current_auth_user),
):
    iat = payload.get("iat")
    return {
        "username": user.username,
        "email": user.email,
        "logged_in_at": iat,
    }