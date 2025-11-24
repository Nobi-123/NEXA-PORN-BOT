from pyrogram import filters
from pyrogram.types import CallbackQuery
from utils.buttons import category_keyboard
from utils.limiter import get_remaining, consume
from utils.logger import log_event

CATEGORY_CHANNELS = {
    "japanese": -1003494008640,
    "hentai": -1003230238714,
    "indian": -1003450553119,
    "russian": -1003365806689,
    "african": -1003236339201
}

def register_video(app):

    @app.on_callback_query()
    async def callback_router(client, callback: CallbackQuery):
        data = callback.data
        uid = callback.from_user.id

        if data == "menu_categories":
            await callback.message.reply_text(
                "🎬 Choose a category:",
                reply_markup=category_keyboard()
            )
            await callback.answer()
            return

        if data.startswith("cat_"):
            category = data.split("_")[1].lower()

            if category not in CATEGORY_CHANNELS:
                await callback.answer("⚠️ Invalid category.", show_alert=True)
                return

            channel_id = CATEGORY_CHANNELS[category]

            remaining, bonus, watched_count = get_remaining(uid)
            if remaining <= 0:
                await callback.answer("⚠️ You reached your daily limit.", show_alert=True)
                return

            try:
                async for msg in client.get_chat_history(channel_id, limit=50):
                    if msg.video:
                        video_msg = msg
                        break
                else:
                    await callback.answer("⚠️ No video found in this channel.", show_alert=True)
                    return
            except Exception as e:
                await callback.answer("⚠️ Failed to get video.", show_alert=True)
                await log_event(f"Failed to fetch from channel {channel_id}: {e}", client)
                return

            ok, mode = consume(uid, str(video_msg.id))
            if not ok:
                await callback.answer("⚠️ Could not consume quota.", show_alert=True)
                return

            try:
                await callback.answer("📤 Sending video...")

                await client.copy_message(
                    chat_id=uid,
                    from_chat_id=channel_id,
                    message_id=video_msg.id
                )

                await log_event(
                    f"User {uid} received video {video_msg.id} from {category}",
                    client
                )

            except Exception as e:
                await callback.answer("⚠️ Failed to send video.", show_alert=True)
                await log_event(
                    f"Copying failed for user {uid}: {e}",
                    client
                )
                return