"""CRUD interfaces for user models"""

from api_v1.users.schemas import CreateUser


def create_user(user_in: CreateUser) -> dict:
    """Create interface for User

    Args:
        user_in (CreateUser): CreateUser instance representing a user to add

    Returns:
        dict: json with success status and user fields as dict
    """
    user = user_in.model_dump()
    return {"success": True, "user": user}
