from pyrogram import filters
from pyrogram.types import CallbackQuery
from database import videos
from utils.buttons import category_keyboard
from utils.limiter import get_remaining, consume
from utils.logger import log_event

def register_video(app):
    @app.on_callback_query()
    async def callback_router(client, callback: CallbackQuery):
        data = callback.data
        uid = callback.from_user.id

        # ---------------- Show category menu ----------------
        if data == "menu_categories":
            await callback.message.reply_text(
                "🎬 Choose a category:",
                reply_markup=category_keyboard()
            )
            await callback.answer()
            return

        # ---------------- Handle category selection ----------------
        if data and data.startswith("cat_"):
            category = data.split("_", 1)[1]

            # Fetch video from DB
            if category == "random":
                doc = videos.aggregate([{"$sample": {"size": 1}}])
            else:
                doc = videos.aggregate([
                    {"$match": {"category": category}},
                    {"$sample": {"size": 1}}
                ])
            try:
                video = next(doc)
            except StopIteration:
                await callback.answer("⚠️ No videos available in this category.", show_alert=True)
                return

            # Check remaining daily limit
            remaining, bonus, watched_count = get_remaining(uid)
            if remaining <= 0:
                await callback.answer(
                    "⚠️ You reached your daily limit of 6 videos.\nInvite friends to get bonus videos!",
                    show_alert=True
                )
                return

            # Consume a video slot
            ok, mode = consume(uid, video["_id"])
            if not ok:
                await callback.answer("⚠️ Could not consume your quota.", show_alert=True)
                return

            # ---------------- Send video ----------------
            try:
                await client.send_video(
                    chat_id=uid,
                    video=video["file_id"],
                    caption=video.get("title", ""),
                )
                await callback.answer("✅ Enjoy your video!")
                # Await async logger
                await log_event(
                    f"User {uid} watched video {video.get('_id')} ({video.get('category')})",
                    client
                )
            except Exception as e:
                await callback.answer("⚠️ Failed to send video.", show_alert=True)
                await log_event(
                    f"Failed to send video {video.get('_id')} to {uid}: {e}",
                    client
                )