from pyrogram import filters
from pyrogram.types import Message
from database import videos
from config import SOURCE_CHANNELS
from utils.logger import log_event

def register_scraper(app):
    @app.on_message(filters.chat(list(SOURCE_CHANNELS.keys())) & (filters.video | filters.document))
    async def index_channel_post(client, message: Message):
        """
        Triggered when a new video or document is posted in a source channel.
        Saves the file in the 'videos' collection if not already indexed.
        """

        # Determine category from SOURCE_CHANNELS
        chat_id = str(message.chat.id)
        category = SOURCE_CHANNELS.get(chat_id, "unknown")

        # Determine file_id
        file_id = None
        if message.video:
            file_id = message.video.file_id
        elif message.document:
            file_id = message.document.file_id

        if not file_id:
            await log_event(f"❌ No valid video/document in message {message.message_id} from {chat_id}", client)
            return

        # Avoid duplicates
        exists = videos.find_one({"source_id": chat_id, "message_id": message.message_id})
        if exists:
            return

        try:
            # Save to MongoDB
            videos.insert_one({
                "file_id": file_id,
                "category": category,
                "title": message.caption or "",
                "source_id": chat_id,
                "message_id": message.message_id,
                "added_at": message.date
            })

            await log_event(
                f"✅ Indexed video from channel {chat_id} (msg {message.message_id}) -> category: {category}",
                client
            )

        except Exception as e:
            await log_event(f"❌ Failed to save video {message.message_id} from {chat_id}: {e}", client)