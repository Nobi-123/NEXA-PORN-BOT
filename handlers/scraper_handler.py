from pyrogram import filters
from pyrogram.types import Message
from database import videos
from config import SOURCE_CHANNELS
from utils.logger import log_event

def register_scraper(app):
    @app.on_message(
        filters.chat(list(SOURCE_CHANNELS.keys())) &
        (filters.video | filters.document)
    )
    async def index_media_channel(client, message: Message):

        file_id = message.video.file_id if message.video else message.document.file_id
        if not file_id:
            return

        # avoid duplicates
        if videos.find_one({"message_id": message.message_id}):
            return

        # auto-detect correct category based on channel ID
        category = SOURCE_CHANNELS.get(str(message.chat.id), "unknown")

        videos.insert_one({
            "file_id": file_id,
            "category": category,
            "title": message.caption or "",
            "source_id": message.chat.id,
            "message_id": message.message_id,
            "added_at": message.date
        })

        await log_event(f"Indexed video in category {category}", client)
