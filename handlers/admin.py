from pyrogram import filters
from pyrogram.types import Message
from database import users, watches, videos, referrals, bot_logs
from utils.logger import log_event
from config import OWNER_IDS
from datetime import datetime, timedelta

def register_admin(app):
    # Show bot statistics
    @app.on_message(filters.command("stats") & filters.user(OWNER_IDS))
    async def cmd_stats(client, message: Message):
        total_users = users.count_documents({})
        active_24h = watches.count_documents({"watched_at": {"$gte": datetime.utcnow() - timedelta(hours=24)}})
        total_videos = videos.count_documents({})
        total_referrals = referrals.count_documents({})

        text = (
            f"📊 Bot Statistics\n\n"
            f"👥 Total Users: `{total_users}`\n"
            f"🔥 Active (24h): `{active_24h}`\n"
            f"🎬 Videos Indexed: `{total_videos}`\n"
            f"🎁 Referrals: `{total_referrals}`\n"
        )
        await message.reply(text)

    # Broadcast a message to all users
    @app.on_message(filters.command("broadcast") & filters.user(OWNER_IDS))
    async def cmd_broadcast(client, message: Message):
        text = message.text.partition(" ")[2]
        if not text:
            return await message.reply("Usage: /broadcast Your message here")

        sent = 0
        for u in users.find({}, {"_id": 1}):
            try:
                await client.send_message(u["_id"], text)
                sent += 1
            except Exception:
                pass

        await message.reply(f"✅ Broadcast sent to {sent} users")
        log_event(f"Broadcast sent to {sent} users", client)

    # Reset user's daily video limit
    @app.on_message(filters.command("resetlimit") & filters.user(OWNER_IDS))
    async def cmd_resetlimit(client, message: Message):
        args = message.text.split()
        if len(args) < 2:
            return await message.reply("Usage: /resetlimit <user_id>")
        uid = int(args[1])
        watches.delete_many({"user_id": uid})
        await message.reply(f"✅ Limit reset for user {uid}")
        log_event(f"Limit reset by admin for {uid}", client)
