"""
Dependencies for problems router
"""

from .schemas import DifficultyLevel, Topic


def get_filters_from_request(
    difficulty_level: DifficultyLevel | None = None, topic: Topic | None = None
) -> dict[str, str]:
    """
    Return filters dict for constructing mongo request
    """
    filters = {}
    if difficulty_level:
        filters["difficulty_level"] = difficulty_level.value
    if topic:
        filters["topic_tagged_text"] = topic.value

    return filters
