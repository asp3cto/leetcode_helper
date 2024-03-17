from beanie import Document

class UsersProblem(Document):
    """Class-document for mongo collection "users_problems"
    """
    id: int
    problem_id: int
    status: str
    solves: list[int] | None

    class Settings:
        """Class for configure mongo collection"""
        
        name = "users_problems"
        keep_nulls = False
