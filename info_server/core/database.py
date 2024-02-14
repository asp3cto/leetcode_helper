# temp_file for create collection "problems" in mongo
import motor.motor_asyncio as mo

# ToDO: change pass argument
mongoClient = mo.AsyncIOMotorClient(
    host="mongo", port=27017, username="problems", password="sosibibu"
)

db = mongoClient.problems_data
problems_collection = db["problems"]
