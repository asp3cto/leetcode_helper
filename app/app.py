"""Main project file"""

from contextlib import asynccontextmanager
from fastapi import FastAPI

from core.models.user import User

from core.models import Base, db_helper


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


@app.get("/")
async def root():
    """temp test"""
    return {"message": "Hello World!"}
