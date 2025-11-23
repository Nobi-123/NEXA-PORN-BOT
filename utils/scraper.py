from pyrogram import Client
from database import videos
import config

app = Client(
    "scraper",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN
)

def scan_channel(channel, limit=200):
    """
    Scans the channel history and adds videos to MongoDB
    """
    with app:
        for m in app.get_chat_history(channel, limit=limit):
            if m.video:
                exists = videos.find_one({"source_id": m.chat.id, "message_id": m.message_id})
                if not exists:
                    videos.insert_one({
                        "file_id": m.video.file_id,
                        "category": config.SOURCE_CHANNELS.get(str(m.chat.username) or str(m.chat.id), "unknown"),
                        "title": m.caption or "",
                        "source_id": m.chat.id,
                        "message_id": m.message_id,
                        "added_at": m.date
                    })
                    print(f"Inserted video {m.message_id} from {channel}")

if __name__ == "__main__":
    # Scan all source channels
    for ch in config.FORCE_CHANNELS:  # or SOURCE_CHANNELS.keys()
        print(f"Scanning channel {ch}...")
        scan_channel(ch, limit=500)
