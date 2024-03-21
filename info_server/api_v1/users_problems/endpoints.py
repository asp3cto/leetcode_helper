"""
Module with enpoints of user's problems router
"""

import requests
from typing import Annotated

from fastapi import APIRouter, Depends, Cookie, HTTPException, status

from core import settings
from .crud import (
    get_user_problems,
    add_solve_to_problem,
    create_user_problem,
    delete_problem,
)
from .schemas import ProblemStatus


router = APIRouter(
    tags=["user_problems"],
)


async def user_id_from_cookie(access_token: Annotated[str | None, Cookie()] = None):
    """Function for check user's session and get his id"""
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

    return response.json().get("user_id")


@router.get("/")
async def home(user_id: int = Depends(user_id_from_cookie)):
    user_problems = await get_user_problems(user_id=user_id)
    if user_problems is None:
        return {"detail": "list is empty"}
    return user_problems


@router.post("/add-problem/")
async def add_problem(
    problem_id: int,
    status: ProblemStatus,
    solve: str | None = None,
    user_id: int = Depends(user_id_from_cookie),
):
    await create_user_problem(
        user_id=user_id, problem_id=problem_id, solve=solve, status=status
    )


@router.post("/{problem_id}/add-solve/")
async def add_solve(
    problem_id: int, new_solve: str, user_id: int = Depends(user_id_from_cookie)
):
    result = await add_solve_to_problem(
        user_id=user_id, problem_id=problem_id, new_solve=new_solve
    )
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return {"detail": result}


@router.delete("/del-problem/")
async def del_problem(problem_id: int, user_id: int = Depends(user_id_from_cookie)):
    result = await delete_problem(user_id=user_id, problem_id=problem_id)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return {"detail": result}
