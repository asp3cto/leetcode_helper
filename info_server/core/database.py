# temp_file for create collection "problems" in mongo
from motor.motor_asyncio import AsyncIOMotorClient

# ToDO: change pass argument
def create_problems_collection():
    mongoClient = AsyncIOMotorClient(
        host="mongo", port=27017, username="problems", password="sosibibu"
    )
    database = mongoClient["problems_data"]
    database["problems"]
    return mongoClient