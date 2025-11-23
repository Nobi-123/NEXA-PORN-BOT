from pyrogram import filters
from pyrogram.types import Message
from database import videos
from config import MEDIA_CHANNEL
from utils.logger import log_event

def register_scraper(app):
    @app.on_message(filters.chat(MEDIA_CHANNEL) & (filters.video | filters.document))
    async def index_media_channel(client, message: Message):
        file_id = message.video.file_id if message.video else message.document.file_id
        if not file_id: return

        if videos.find_one({"message_id": message.message_id}):
            return

        videos.insert_one({
            "file_id": file_id,
            "category": "unknown",  
            "title": message.caption or "",
            "source_id": message.chat.id,
            "message_id": message.message_id,
            "added_at": message.date
        })

        await log_event(f"Indexed video {file_id} in media channel", client)