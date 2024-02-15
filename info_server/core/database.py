# temp_file for create collection "problems" in mongo
import motor.motor_asyncio as mo
from core.config import settings
# ToDO: change pass argument
mongoClient = mo.AsyncIOMotorClient(
    settings.db_url
)

db = mongoClient.problems_data
problems_collection = db["problems"]
