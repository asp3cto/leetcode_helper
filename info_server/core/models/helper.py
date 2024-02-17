"""
Utils for MongoDB
"""

import csv

from motor.motor_asyncio import AsyncIOMotorClient
from motor.core import AgnosticClient, AgnosticCollection
from beanie import init_beanie
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
            for each in reader:
                row = {}
                for field in reader.fieldnames:
                    if field == "Question ID":
                        row["id"] = each[field]
                        continue
                    valid_key = field.lower().replace(" ", "_")
                    if each[field]:
                        if (
                            valid_key == "similar_questions_id"
                            or valid_key == "similar_questions_text"
                        ):
                            row[valid_key] = [
                                int(elem) if elem.isdigit() else elem
                                for elem in each[field].split(",")
                            ]
                        else:
                            row[valid_key] = each[field]
                problem_list.append(row)
        return problem_list

    @staticmethod
    async def fill_problems_collection():
        problems: list[dict] = MongoDBHelper._parse_csv_data()
        for problem in problems:
            problem_doc = Problem(**problem)
            await Problem.insert_one(problem_doc)


mongodb_helper = MongoDBHelper()
