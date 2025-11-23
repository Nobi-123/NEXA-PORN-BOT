from pymongo import MongoClient, ASCENDING
from config import MONGO_URL

# Connect to MongoDB
client = MongoClient(MONGO_URL)
db = client["anime_bot"]

# Collections
users = db["users"]           # Stores user info and referral codes
videos = db["videos"]         # Stores indexed videos
watches = db["watches"]       # Tracks videos watched per user
referrals = db["referrals"]   # Tracks referrals
bot_logs = db["bot_logs"]     # Logs events

# Indexes
# _id is already unique by default, no need for unique=True
users.create_index([("_id", ASCENDING)])  
videos.create_index([("source_id", ASCENDING), ("message_id", ASCENDING)], unique=True)
watches.create_index([("user_id", ASCENDING), ("watched_at", ASCENDING)])
referrals.create_index([("referrer_id", ASCENDING), ("referred_id", ASCENDING)])
bot_logs.create_index([("ts", ASCENDING)])