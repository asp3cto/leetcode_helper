"""
Utils for MongoDB
"""

import csv
from typing import Sequence

from core.config import settings
from core.models.problem import Problem


async def fill_problems_collection():
    problems: list[dict] = parse_csv_data()
    for problem in problems:
        problem_doc = Problem(**problem)
        await Problem.insert_one(problem_doc)


def parse_csv_data() -> list[dict]:
    """Parse csv file for collection "problems"

    Returns:
        list[dict]: list of dicts from csv file
    """
    problem_list = []
    with open(settings.csv_file, "r") as csvFile:
        reader = csv.DictReader(csvFile)
        for record in reader:
            row = parse_row_from_csv(reader.fieldnames, record)
            problem_list.append(row)
    return problem_list


def parse_row_from_csv(fieldnames: Sequence[str], record: dict) -> dict:
    result = {}
    for field_name in fieldnames:
        if field_name == "Question ID":
            result["id"] = record[field_name]
            continue
        valid_key = field_name.lower().replace(" ", "_")
        if record[field_name]:
            if valid_key == "similar_questions_id":
                result[valid_key] = [
                    int(elem) for elem in record[field_name].split(",")
                ]
            elif valid_key == "similar_questions_text":
                result[valid_key] = record[field_name].split(",")
            else:
                result[valid_key] = record[field_name]
    return result


async def check_problems_collection_is_empty() -> bool:
    return not await Problem.count()
