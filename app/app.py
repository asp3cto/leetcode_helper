"""Main project file"""

from contextlib import asynccontextmanager
from fastapi import FastAPI

from core.models import Base, db_helper

from api_v1.users.views import (
    auth_router,
    register_router,
    reset_password_router,
    users_router,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """On startup function to create tables

    Args:
        app (FastAPI): main app
    """
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)
# set requires_verification to True to allow only verified users to login
app.include_router(
    auth_router,
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    register_router,
    prefix="/register",
    tags=["auth"],
)
app.include_router(reset_password_router, prefix="/reset_password", tags=["auth"])
app.include_router(users_router, prefix="/users", tags=["auth"])


@app.get("/")
async def root():
    """temp test"""
    return {"message": "Hello World!"}
