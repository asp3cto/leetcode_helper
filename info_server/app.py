import requests

from functools import wraps
from typing import Annotated, Any, Callable, Optional
from fastapi import Cookie, FastAPI, Response, HTTPException, status, Request, Depends

from core import settings

# temp
import core.models.helper as helper

app = FastAPI(openapi_prefix="/info")


def auth_required(func: Callable) -> Callable:
    @wraps(func)
    async def wrapper(*args: Any, **kwargs: Any):
        try:
            refresh_token = kwargs.get("refresh_token")
            access_token = kwargs.get("access_token")
            if not (refresh_token and access_token):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="user is not logged in",
                )

            response = requests.get(
                url=settings.validate_token_endpoint,
                cookies={"access_token": access_token, "refresh_token": refresh_token},
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
    refresh_token: Annotated[str | None, Cookie()] = None,
):
    return {"detail": "only for logged in users hehe"}


# for test csv, temp
@app.get("/mongocsv")
async def get_mongot():
    helper.csv_to_mongo("./data/problems.csv")
    return {"detail": "gj"}
