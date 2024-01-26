"""Main project file"""

from contextlib import asynccontextmanager
from fastapi import FastAPI

from core.models import Base, db_helper

from api_v1.users.views import router as apiv1_users_router


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
app.include_router(apiv1_users_router)


@app.get("/")
async def root():
    """temp test"""
    return {"message": "Hello World!"}
