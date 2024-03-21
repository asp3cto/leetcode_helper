"""
Operations for mongo collections users_problems
"""

from beanie.exceptions import DocumentNotFound

from core.models import UserProblem
from .schemas import ProblemStatus


async def create_user_problem(
    user_id: int,
    problem_id: int,
    solve: str | None,
    status: ProblemStatus = ProblemStatus.planned,
) -> None:
    """Function for create(save)
      problem for user's collection of problems

    Args:
        user_id (int): id's user
        problem_id (int): link to problem, which in problems collection
        status (ProblemStatus): status planned to solve or solved problem
        solve (str | None): solve of problem
    """
    solves = [solve]
    user_problem = UserProblem(
        user_id=user_id, problem_id=problem_id, status=status, solves=solves
    )
    await user_problem.insert()


async def add_solve_to_problem(
    user_id: int, problem_id: int, new_solve: str
) -> str | None:
    """Function for add solve to problem

    Args:
        user_id (int): id's user
        problem_id (int): link to problem, which in problems collection
        new_solve (str): solve of problem

    Returns:
        str | None: return success string or None if fail
    """
    user_solves = await UserProblem.find_one(
        UserProblem.user_id == user_id, UserProblem.problem_id == problem_id
    )
    user_solves.solves.append(new_solve)
    try:
        await user_solves.replace()
        return "success operation add solve"
    except (ValueError, DocumentNotFound):
        return None


async def get_user_problems(
    user_id: int,
) -> list[UserProblem] | None:
    """Function for get user's problems

    Args:
        user_id (int): id's user

    Returns:
        list[UserProblem] | None: if not empty return list
    """
    user_problems = await UserProblem.find_many(
        UserProblem.user_id == user_id
    ).to_list()
    if len(user_problems) != 0:
        return user_problems


async def delete_problem(user_id: int, problem_id: int) -> str | None:
    """Function for delete problem from user's problems collection

    Args:
        user_id (int): id's user
        problem_id (int): link to problem, which in problems collection

    Returns:
        str | None: none if operation fail
    """
    result = await UserProblem.find_one(
        UserProblem.user_id == user_id, UserProblem.problem_id == problem_id
    ).delete()
    if result.deleted_count() == 1:
        return "success operation delete"
