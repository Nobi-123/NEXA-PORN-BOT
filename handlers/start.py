from pyrogram import filters
from pyrogram.types import Message
import secrets
from database import users, referrals
from utils.fsub import check_sub
from utils.buttons import main_keyboard, join_buttons
from utils.logger import log_event
from config import FORCE_CHANNELS, START_TEXT, START_IMAGE, REFERRAL_BONUS

def register_start(app):
    @app.on_message(filters.private & filters.command("start"))
    async def start_handler(client, message: Message):
        user = message.from_user
        args = message.text.split()

        # Create user
        if not users.find_one({"_id": user.id}):
            code = secrets.token_urlsafe(8)
            users.insert_one({
                "_id": user.id,
                "username": user.username,
                "first_name": user.first_name,
                "created_at": message.date,
                "referral_code": code,
                "bonus": 0
            })
            await log_event(f"New user started: {user.id} ({user.username})", client)

        # Referral
        if len(args) > 1 and args[1].startswith("ref_"):
            ref_code = args[1][4:]
            ref_user = users.find_one({"referral_code": ref_code})
            if ref_user and ref_user["_id"] != user.id:
                referrals.insert_one({
                    "referrer_id": ref_user["_id"],
                    "referred_id": user.id,
                    "credited": False
                })

        # Force join
        sub = await check_sub(client, user.id, FORCE_CHANNELS)
        if sub is not True:
            await message.reply(
                "⚠️ You must join the mandatory channels to use this bot.",
                reply_markup=join_buttons(FORCE_CHANNELS)
            )
            return

        # Send welcome
        try:
            await client.send_photo(
                chat_id=user.id,
                photo=START_IMAGE,
                caption=START_TEXT.format(first_name=user.first_name, username=user.username),
                reply_markup=main_keyboard()
            )
        except:
            await message.reply(
                START_TEXT.format(first_name=user.first_name, username=user.username),
                reply_markup=main_keyboard()
            )