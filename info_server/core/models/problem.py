"""Class-document for mongo collection "problems"
"""

from beanie import Document


class Problem(Document):
    """Class-document for mongo collection "problems" """

    id: int
    question_title: str
    question_slug: str
    question_text: str | None = None
    topic_tagged_text: str | None = None
    difficulty_level: str | None = None
    success_rate: float | None = None
    total_submission: int | None = None
    total_accepted: int | None = None
    likes: int | None = None
    dislikes: int | None = None
    hints: str | None = None
    similar_questions_id: list[int] | None = None
    similar_questions_text: list[str] | None = None

    class Settings:
        """Class for configure mongo collection"""

        name = "problems"
        keep_nulls = False
