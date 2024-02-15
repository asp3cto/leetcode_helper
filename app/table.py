from fastapi import APIRouter, Path

router = APIRouter(prefix="/table", tags=["Table"])


@router.get("/")
async def table():
    pass
