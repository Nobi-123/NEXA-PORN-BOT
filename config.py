import os
from dotenv import load_dotenv

load_dotenv()

# ---------------- Telegram Bot ----------------
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_ID = int(os.getenv("API_ID", "21134445"))
API_HASH = os.getenv("API_HASH", "231c18ea7273824491d6bf05425ab74e")

# ---------------- MongoDB ----------------
MONGO_URL = os.getenv("MONGO_URL", "mongodb+srv://SickNessRoBot:Sickness@sickness.qxwkdjl.mongodb.net/?appName=Sickness")

# ---------------- Bot Owners ----------------
OWNER_IDS = list(map(int, os.getenv("OWNER_IDS", "").split(",")))

MEDIA_CHANNEL = "@MEDIAxNEXA"  # Bot-owned channel to store videos

# ---------------- Log Channel ----------------
LOG_CHANNEL = os.getenv("LOG_CHANNEL", "-1003313190368")  # Optional, channel to log user events

# ---------------- Daily Limits ----------------
DAILY_LIMIT = 6        # Free videos per 12 hours
REFRESH_HOURS = 12     # Daily limit refresh interval
REFERRAL_BONUS = 3     # Extra videos per referral

# ---------------- Start Message ----------------
START_TEXT = (
    "👋 Hello {first_name}!\n\n"
    "Welcome to Porn Video Bot.\n\n"
    "🎬 Watch 6 free Porns videos daily.\n"
    "Invite friends to get bonus videos! 💖"
)
START_IMAGE = "https://telegra.ph/file/abcd1234efgh5678.png"  # Replace with your welcome image URL or Telegram file_id

# ---------------- Channels ----------------
# FORCE_CHANNELS: users must join these channels to use the bot
FORCE_CHANNELS = [
    "NexaCoders",
    "NexaMeetup"
]

# SOURCE_CHANNELS: channel username/id -> category name mapping
SOURCE_CHANNELS = {
    "NEXAxHENTAI": "hentai",
    "NEXAxJAPANESE": "japanese",
    "NEXAxRUSSIAN": "russian",
    "NEXAxINDIAN": "indian",
    "NEXAxAFRICAN": "african"
}
