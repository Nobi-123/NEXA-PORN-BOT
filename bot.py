from pyrogram import Client
from handlers import register_handlers
from config import BOT_TOKEN, API_ID, API_HASH

# ---------------- Create Pyrogram Client ----------------
app = Client(
    "anime_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# ---------------- Register All Handlers ----------------
register_handlers(app)

# ---------------- Start Bot ----------------
if __name__ == "__main__":
    print("🤖 Lee Bsdk Telegram Bot is starting...")
    app.run()
