import requests

from functools import wraps
from typing import Annotated, Any, Callable, Optional
from fastapi import Cookie, FastAPI, Response, HTTPException, status

from core import settings

app = FastAPI()


def auth_required(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any):
        try:
            if not (access_token := kwargs.get("access_token")):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="user is not logged in",
                )
             
            response = requests.get(
                url=settings.validate_token_endpoint,
                cookies={"access_token": access_token}
            )
            
            response.raise_for_status()
            return func(*args, **kwargs)
        except requests.HTTPError as error:
            return Response(
               status_code=error.response.status_code
            )

    return wrapper


@app.get("/")
@auth_required
async def home(access_token: Annotated[str | None, Cookie()] = None):
    return {"detail": "only for logged in users hehe"}
