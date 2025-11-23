from pymongo import MongoClient, ASCENDING
from config import MONGO_URL

client = MongoClient(MONGO_URL)
db = client["anime_bot"]

users = db["users"]
referrals = db["referrals"]
videos = db["videos"]
bot_logs = db["bot_logs"]
limits = db["limits"]
watches = db["watches"]  # <--- Added

# Indexes
users.create_index([("_id", ASCENDING)])
videos.create_index([("file_id", ASCENDING)], unique=True)
limits.create_index([("_id", ASCENDING)])
watches.create_index([("_id", ASCENDING)])