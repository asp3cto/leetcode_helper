"""
Module with endpoints of problems router
"""

from fastapi import APIRouter
from fastapi_pagination import Page
from fastapi_pagination.ext.beanie import paginate

from core.models import Problem
from .schemas import ProblemSchemaFull, ProblemSchemaShort


router = APIRouter(
    tags=["problems"],
)


@router.get("/full/")
async def get_all_problems_full_repr_pagination() -> Page[ProblemSchemaFull]:
    return await paginate(Problem.find_all())


@router.get("/short/")
async def get_all_problems_short_repr_pagination() -> Page[ProblemSchemaShort]:
    return await paginate(Problem.find_all())
