from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb://localhost:27017"
DATABASE_NAME = "State_News"

client = AsyncIOMotorClient(MONGO_URL)
db = client[DATABASE_NAME]

role_collection = db["roles"]
user_collection = db["users"]
state_collection = db["states"]
city_collection = db["cities"]
area_collection = db["areas"]
news_collection = db["news"]
comment_collection = db["comments"]
badge_collection = db["badges"]
achivment_collection = db["achivments"]
