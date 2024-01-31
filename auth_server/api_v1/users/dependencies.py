"Dependencies for endpoints.py"
from typing import Annotated

from fastapi import Cookie, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from jwt import ExpiredSignatureError, InvalidTokenError


from core.models import pg_db_helper, User
from auth.utils import decode_jwt, encode_jwt, validate_password
from api_v1.users.crud import get_user_by_username, get_user_by_id


async def validate_auth_user_password(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(pg_db_helper.get_scoped_session),
):
    """
    Helper Function for login route to check a user by password
    """
    invalid_login_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password",
    )
    user_from_db = await get_user_by_username(
        session=session, username=form_data.username
    )

    # if no user was found by username in db
    if not user_from_db:
        raise invalid_login_exception

    hash_from_db: bytes = user_from_db.hashed_password

    # if passwords dont match
    if not validate_password(form_data.password, hash_from_db):
        raise invalid_login_exception

    if not user_from_db.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="User is not active"
        )

    return user_from_db


async def validate_tokens(
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


async def get_current_refresh_token_payload(
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

    user_from_db = await get_user_by_id(session=session, user_id=id)
    # if no user was found by username in db
    if not user_from_db:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            # NOTE: REMOVE ADDITIONAL INFO IN PROD
            detail="token invalid (user not found)",
        )
    if user_from_db.is_active:
        return user_from_db
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="user inactive",
    )
