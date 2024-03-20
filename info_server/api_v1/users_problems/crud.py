from .schemas import ProblemStatus
from core.models import UserProblem
from beanie.exceptions import DocumentNotFound

async def create_user_problem(
        user_id: int,
        problem_id: int,
        status: ProblemStatus,
        solve: str | None
) -> None:
    solves = [solve]
    user_problem =  UserProblem(user_id=user_id, problem_id=problem_id, status=status, solves=solves)
    await user_problem.insert()


async def add_solve_to_problem(
       user_id: int,
       problem_id: int,
       new_solve: str 
)->None:
    user_solves = await UserProblem.find_one(UserProblem.user_id==user_id,UserProblem.problem_id==problem_id)
    print(user_solves)
    user_solves.solves.append(new_solve)
    try:
        await user_solves.replace()
    except (ValueError, DocumentNotFound):
        print("Can't replace a non existing document") 
    

async def get_user_problems(
        user_id: int,
) -> list[UserProblem] | None:
    user_problems = await UserProblem.find_many(UserProblem.user_id==user_id).to_list()
    return user_problems


async def delete_problem(
        user_id: int,
        problem_id: int
) -> None:
    await UserProblem.find_one(UserProblem.user_id==user_id,UserProblem.problem_id==problem_id).delete()
