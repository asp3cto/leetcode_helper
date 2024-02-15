# temp_file for create collection "problems" in mongo
<<<<<<< HEAD
from motor.motor_asyncio import AsyncIOMotorClient

# ToDO: change pass argument
def create_problems_collection():
    mongoClient = AsyncIOMotorClient(
        host="mongo", port=27017, username="problems", password="sosibibu"
    )
    database = mongoClient["problems_data"]
    database["problems"]
    return mongoClient
=======
import motor.motor_asyncio as mo
from core.config import settings
# ToDO: change pass argument
mongoClient = mo.AsyncIOMotorClient(
    settings.db_url
)

db = mongoClient.problems_data
problems_collection = db["problems"]
>>>>>>> 13afb68
