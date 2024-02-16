from typing import Optional

import pymongo
from pydantic import Field
from beanie import Document


class Problem(Document):
    id: int
    question_title: str
    question_slug: str
    question_text: str
    topic_tagged_text: str | None
    difficulty_level: str | None
    success_rate: float | None
    total_submission: int | None
    total_accepted: int | None
    likes: int | None
    dislikes: int | None
    hints: str | None
    similar_questions_id: list[int] | None
    similar_questions_text: list[str] | None

    class Settings:
        name = "problems"
        keep_nulls = False
