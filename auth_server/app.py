"""Main project file"""

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


app = FastAPI(lifespan=lifespan)
app.include_router(users_router, prefix="/auth")
