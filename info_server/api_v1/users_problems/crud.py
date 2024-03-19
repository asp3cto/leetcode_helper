from schemas import ProblemStatus
from core.models import UserProblem
from beanie.exceptions import DocumentNotFound

async def create_user_problem(
        user_id: int,
        problem_id: int,
        status: ProblemStatus,
        solve: str | None
) -> None:
    solves = [solve]
    UserProblem(user_id=user_id, problem_id=problem_id, status=status, solves=solves).insert()

async def add_solve_to_problem(
       user_id: int,
       problem_id: int,
       new_solve: str 
)->None:
    user_solves = await UserProblem.find_one(UserProblem.user_id==user_id,UserProblem.problem_id==problem_id)
    user_solves.solves.append(new_solve)
    try:
        user_solves.replace()
    except (ValueError, DocumentNotFound):
        print("Can't replace a non existing document") 
    

async def get_user_problems(
        user_id: int,
) -> list[UserProblem] | None:
    return await UserProblem.find_all(UserProblem.user_id==user_id).to_list()


async def update_user_problems():
    pass


async def edit_solve_problem():
    pass