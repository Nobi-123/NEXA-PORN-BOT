import os
from dotenv import load_dotenv

load_dotenv()

# ---------------- Telegram Bot ----------------
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")

# ---------------- MongoDB ----------------
MONGO_URL = os.getenv("MONGO_URL")

# ---------------- Bot Owners ----------------
OWNER_IDS = list(map(int, os.getenv("OWNER_IDS", "").split(",")))

# ---------------- Log Channel ----------------
LOG_CHANNEL = os.getenv("LOG_CHANNEL")  # Optional, channel to log user events

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
    "@hentai_channel",
    "@japanese_channel",
    "@russian_channel",
    "@indian_channel",
    "@korean_channel",
    "@african_channel"
]

# SOURCE_CHANNELS: channel username/id -> category name mapping
SOURCE_CHANNELS = {
    "@hentai_channel": "hentai",
    "@japanese_channel": "japanese",
    "@russian_channel": "russian",
    "@indian_channel": "indian",
    "@korean_channel": "korean",
    "@african_channel": "african"
}
