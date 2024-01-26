"""Module with auth utils"""

import uuid

from fastapi import Depends
from fastapi_users.authentication import (
    CookieTransport,
    AuthenticationBackend,
    JWTStrategy,
)
from fastapi_users import BaseUserManager, IntegerIDMixin

from .config import settings
from .models import User, get_user_db

cookie_transport = CookieTransport(cookie_max_age=3600)


def get_jwt_strategy() -> JWTStrategy:
    """Creates an instance of JWT strategy
    By default encryption algorithm is set to HS256
    Returns:
        JWTStrategy: instance of strategy
    """
    return JWTStrategy(secret=settings.jwt_secret, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = settings.jwt_secret
    verification_token_secret = settings.jwt_secret

    """async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"Verification requested for user {user.id}. Verification token: {token}")"""


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
