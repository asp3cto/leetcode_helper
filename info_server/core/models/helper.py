"""
Utils for MongoDB
"""

import csv

from motor.motor_asyncio import AsyncIOMotorClient
from motor.core import AgnosticClient, AgnosticCollection

from core.config import settings


def csv_to_mongo(filename: str, collection: AgnosticCollection):
    """Import csv data to MongoDB

    Args:
        filename (str): Path to csv file
        collection (AgnosticCollection): Collection of MongoDB
    """
    with open(filename, "r") as csvFile:
        reader = csv.DictReader(csvFile)
        for each in reader:
            row = {}
            for field in reader.fieldnames:
                if each[field] != "":
                    row[field] = each[field]
            collection.insert_one(row)


def create_problems_collection() -> AgnosticClient:
    """Create problems collection in MongoDB

    Returns:
        AgnosticClient: MongoDB client
    """
    mongoClient = AsyncIOMotorClient(settings.db_url)
    database = mongoClient["problems_data"]
    problems_collection = database["problems"]
    csv_to_mongo(settings.csv_file, problems_collection)

    return mongoClient
