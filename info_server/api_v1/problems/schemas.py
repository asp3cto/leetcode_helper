"""
Schemas for problems route
"""

from pydantic import BaseModel, Field, HttpUrl, computed_field, root_validator, validator


class ProblemSchemaBase(BaseModel):
    """
    Base class for problem schema 
    """
    
    id: int
    question_title: str


class ProblemSchemaShort(ProblemSchemaBase):
    """
    Class with short problem schema for endpoints
    """
    
    difficulty_level: str | None = None
    question_slug: str
    
    @computed_field
    @property
    def url(self) -> int:
        return get_url_from_problem_slug(self.question_slug)


class ProblemSchemaFull(ProblemSchemaShort):
    """
    Class with full problem schema for endpoints
    """

    question_text: str | None = None
    topic_tagged_text: str | None = None
    success_rate: float | None = None
    total_submission: int | None = None
    total_accepted: int | None = None
    likes: int | None = None
    dislikes: int | None = None
    hints: str | None = None
    similar_questions_id: list[int] | None = None
    similar_questions_text: list[str] | None = None


def get_url_from_problem_slug(problem_slug: str):
    return f"https://leetcode.com/problems/{problem_slug}/description/"

