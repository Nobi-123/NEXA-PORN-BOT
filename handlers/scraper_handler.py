from pyrogram import filters
from pyrogram.types import Message
from database import videos
from config import SOURCE_CHANNELS, MEDIA_CHANNEL
from utils.logger import log_event

def register_scraper(app):
    @app.on_message(filters.chat(list(SOURCE_CHANNELS.keys())) & (filters.video | filters.document))
    async def index_channel_post(client, message: Message):
        """
        Forward video/document to bot media channel and save in DB
        """

        chat_id = str(message.chat.id)
        category = SOURCE_CHANNELS.get(chat_id, "unknown").lower()

        # Determine file_id
        file_id = None
        if message.video:
            file_id = message.video.file_id
        elif message.document:
            file_id = message.document.file_id

        if not file_id:
            await log_event(f"No valid media in msg {message.message_id} from {chat_id}", client)
            return

        # Avoid duplicates
        if videos.find_one({"source_id": chat_id, "message_id": message.message_id}):
            return

        try:
            # Forward to bot-owned media channel
            forwarded = await client.forward_messages(
                chat_id=MEDIA_CHANNEL,
                from_chat_id=message.chat.id,
                message_ids=message.message_id
            )

            # Get forwarded file_id
            f_id = forwarded.video.file_id if forwarded.video else forwarded.document.file_id

            videos.insert_one({
                "file_id": f_id,
                "category": category,
                "title": message.caption or "",
                "source_id": chat_id,
                "message_id": message.message_id,
                "added_at": message.date
            })

            await log_event(f"Indexed video {f_id} from {chat_id} -> {category}", client)

        except Exception as e:
            await log_event(f"Error forwarding msg {message.message_id} from {chat_id}: {e}", client)