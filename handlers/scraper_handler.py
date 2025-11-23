from pyrogram import filters
from pyrogram.types import Message
from database import videos
from config import SOURCE_CHANNELS
from utils.logger import log_event

def register_scraper(app):
    @app.on_message(filters.chat(list(SOURCE_CHANNELS.keys())) & filters.video)
    async def index_channel_post(client, message: Message):
        """
        Triggered when a new video is posted in one of the source channels.
        Saves the video in the 'videos' collection if not already indexed.
        """

        # Determine category from channel
        chat_id = str(message.chat.username or message.chat.id)
        category = SOURCE_CHANNELS.get(chat_id) or SOURCE_CHANNELS.get(str(message.chat.id))
        if not category:
            for k, v in SOURCE_CHANNELS.items():
                if str(k) == str(message.chat.id):
                    category = v
                    break

        # Extract video details
        file_id = message.video.file_id
        title = message.caption or ''

        # Avoid duplicates
        exists = videos.find_one({"source_id": message.chat.id, "message_id": message.message_id})
        if not exists:
            videos.insert_one({
                "file_id": file_id,
                "category": category or "unknown",
                "title": title,
                "source_id": message.chat.id,
                "message_id": message.message_id,
                "added_at": message.date
            })
            log_event(f"Indexed video from channel {message.chat.id} (msg {message.message_id}) -> category: {category}", client)
