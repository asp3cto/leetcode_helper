"""CRUD for problems collection"""

from fastapi_pagination.ext.beanie import paginate

from core.models import Problem


async def find_problems_by_filter_with_pagination(filters: dict) -> list:
    return await paginate(Problem.find_many(filters))


async def find_top_problems_with_pagination() -> list:
    return await paginate(Problem.find_many(Problem.id <= 100))
