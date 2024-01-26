"""Endpoints for user"""

from fastapi import APIRouter

from api_v1.users import crud
from api_v1.users.schemas import CreateUser


router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/")
def create_user(user: CreateUser):
    """Endpoint for user creation

    Args:
        user (CreateUser): user object for creation

    Returns:
        dict: status code and user fields as dict
    """
    return crud.create_user(user_in=user)
