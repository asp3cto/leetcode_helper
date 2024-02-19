"""
Module with endpoints of problems router
"""

from fastapi import APIRouter, Depends
from fastapi_pagination import Page

from .schemas import ProblemSchemaFull, ProblemSchemaShort
from .dependencies import get_filters_from_request
from .crud import (
    find_problems_by_filter_with_pagination,
    find_top_problems_with_pagination,
)


router = APIRouter(
    tags=["problems"],
)


@router.get("/full/")
async def get_all_problems_full_repr_pagination_with_filters(
    filters: dict = Depends(get_filters_from_request),
) -> Page[ProblemSchemaFull]:
    return await find_problems_by_filter_with_pagination(filters)


@router.get("/short/")
async def get_all_problems_short_repr_pagination_with_filters(
    filters: dict = Depends(get_filters_from_request),
) -> Page[ProblemSchemaShort]:
    return await find_problems_by_filter_with_pagination(filters)


@router.get("/top100/")
async def get_top_problems_short_repr_pagination_with_filters() -> (
    Page[ProblemSchemaShort]
):
    return await find_top_problems_with_pagination()
