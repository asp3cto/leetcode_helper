"""
Main project module
This app is responsible for all authorization processes
and is based on JWT on cookie with access token
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI

from core.models import Base, pg_db_helper
from api_v1.users import users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """On startup function to create tables

    Args:
        app (FastAPI): main app
    """
    async with pg_db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan, openapi_prefix="/auth")
app.include_router(users_router, prefix="")
