"""
Info server
"""

import requests
from functools import wraps
from typing import Annotated, Any, Callable

from fastapi import Cookie, FastAPI, Response, HTTPException, status

from core import settings, helper


async def lifespan(app: FastAPI):
    """On startup function to create tables

    Args:
        app (FastAPI): main app
    """
    mongoClient = helper.create_problems_collection()
    yield
    mongoClient.close()


app = FastAPI(lifespan=lifespan, openapi_prefix="/info")


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
