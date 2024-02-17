"""
Utils for MongoDB
"""

import csv

from motor.motor_asyncio import AsyncIOMotorClient
from motor.core import AgnosticClient

from core.config import settings
from core.models.problem import Problem


class MongoDBHelper:
    """Class for interacting with the MongoDB"""

    def __init__(self) -> None:
        self._mongoClient = AsyncIOMotorClient(settings.db_url)

    def get_client(self) -> AgnosticClient:
        return self._mongoClient

    @staticmethod
    def _parse_csv_data() -> list[dict]:
        """Parse csv file for collection "problems"

        Returns:
            list[dict]: list of dicts from csv file
        """
        problem_list = []
        with open(settings.csv_file, "r") as csvFile:
            reader = csv.DictReader(csvFile)
            for record in reader:
                row = {}
                for field_name in reader.fieldnames:
                    if field_name == "Question ID":
                        row["id"] = record[field_name]
                        continue
                    valid_key = field_name.lower().replace(" ", "_")
                    if record[field_name]:
                        if (
                            valid_key == "similar_questions_id"
                            or valid_key == "similar_questions_text"
                        ):
                            row[valid_key] = [
                                int(elem) if elem.isdigit() else elem
                                for elem in record[field_name].split(",")
                            ]
                        else:
                            row[valid_key] = record[field_name]
                problem_list.append(row)
        return problem_list

    @staticmethod
    async def fill_problems_collection():
        problems: list[dict] = MongoDBHelper._parse_csv_data()
        for problem in problems:
            problem_doc = Problem(**problem)
            await Problem.insert_one(problem_doc)


mongodb_helper = MongoDBHelper()
