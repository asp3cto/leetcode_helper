"""Endpoints for user"""

import uuid

from fastapi_users import FastAPIUsers

from .schemas import UserCreate, UserRead, UserUpdate

from core import auth_backend, get_user_manager
from core.models import User

fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)

auth_router = fastapi_users.get_auth_router(auth_backend)
register_router = fastapi_users.get_register_router(UserRead, UserCreate)
reset_password_router = fastapi_users.get_reset_password_router()
users_router = fastapi_users.get_users_router(UserRead, UserUpdate)
