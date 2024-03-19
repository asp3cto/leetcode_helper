"""
Info server
"""

import requests
from functools import wraps
from typing import Annotated, Any, Callable
from contextlib import asynccontextmanager

from fastapi import Cookie, FastAPI, Response, HTTPException, status
from fastapi_pagination import add_pagination
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from core import settings
from core.models import helper, Problem, UserProblem
from api_v1.problems import problems_router
from api_v1.users_problems import user_problems_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """On startup function to create tables

    Args:
        app (FastAPI): main app
    """
    mongo_client = AsyncIOMotorClient(settings.db_url)
    await init_beanie(database=mongo_client.mongo, document_models=[Problem, UserProblem])
    if await helper.check_problems_collection_is_empty():
        await helper.fill_problems_collection()
    yield
    mongo_client.close()


app = FastAPI(lifespan=lifespan, openapi_prefix="/info")
app.include_router(problems_router, prefix="/problems")
app.include_router(user_problems_router, prefix="/user-problems")
add_pagination(app)


def auth_required(func: Callable) -> Callable:
    @wraps(func)
    async def wrapper(*args: Any, **kwargs: Any):
        try:
            access_token = kwargs.get("access_token")
            if not access_token:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="user is not logged in",
                )

            response = requests.get(
                url=settings.validate_token_endpoint,
                cookies={"access_token": access_token},
            )

            response.raise_for_status()

            return await func(*args, **kwargs)
        except requests.HTTPError as error:
            return Response(status_code=error.response.status_code)

    return wrapper


@app.get("/")
@auth_required
async def home(
    access_token: Annotated[str | None, Cookie()] = None,
):
    return {"detail": "only for logged in users hehe"}
