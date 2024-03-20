from beanie import Document

class UserProblem(Document):
    """Class-document for mongo collection "users_problems"
    """
    user_id: int
    problem_id: int
    status: str
    solves: list[str] | None = None

    class Settings:
        """Class for configure mongo collection"""
        
        name = "users_problems"
        keep_nulls = False
