from fastapi import APIRouter, Depends, Cookie, HTTPException, status
from typing import Annotated
from core import settings
from .crud import get_user_problems, add_solve_to_problem, create_user_problem, delete_problem
import requests
from .schemas import ProblemStatus

router = APIRouter(
    tags=["user_problems"],
)

async def user_id_from_cookie(access_token: Annotated[str | None, Cookie()] = None):
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
async def home(
    user_id: int = Depends(user_id_from_cookie)
):
    user_problems = await get_user_problems(user_id=user_id)
    return user_problems


@router.post("/add-problem/")
async def add_problem (
    problem_id: int,
    status: ProblemStatus,
    solve: str | None = None,
    user_id: int = Depends(user_id_from_cookie)
):
    try:
        await create_user_problem(user_id=user_id,
                            problem_id=problem_id, 
                            solve=solve,
                            status=status)
        return {"user_id": user_id,
                "problem_id": problem_id,
                "status": "problem added"}
    except Exception:
        return {"detail": "xueta"}

@router.post("/{problem_id}/add-solve/")
async def add_solve(
    problem_id: int,
    new_solve: str,
    user_id: int = Depends(user_id_from_cookie)
):
    await add_solve_to_problem(
        user_id=user_id,
        problem_id=problem_id,
        new_solve=new_solve
    )
    return {"detail": "new solve added"}

@router.delete("/del-problem/")
async def del_problem(
    problem_id: int,
    user_id: int = Depends(user_id_from_cookie)
):
    await delete_problem(user_id=user_id, problem_id=problem_id)
    return {"detail": "delete success"}