from beanie import Document

class Solve(Document):
    """Class-document for mongo collection solves
    """
    id: int
    title: str | None
    description: str | None
    language: str | None
    contents: str

    class Settings:
        """Class for configure mongo collection"""

        name = "solves"
        keep_nulls = False