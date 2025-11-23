from pyrogram import filters
from pyrogram.types import Message
import secrets
from database import users, referrals
from utils.fsub import check_sub
from utils.buttons import main_keyboard, join_buttons
from utils.logger import log_event
from config import REFERRAL_BONUS, START_TEXT, START_IMAGE  # Add these in config.py

def register_start(app):
    @app.on_message(filters.private & filters.command("start"))
    async def start_handler(client, message: Message):
        args = message.text.split()
        user = message.from_user

        # Create user if not exists
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
            log_event(f"New user started: {user.id} ({user.username})", client)

        # Referral param
        if len(args) > 1 and args[1].startswith("ref_"):
            ref = args[1][4:]
            referrer = users.find_one({"referral_code": ref})
            if referrer and referrer["_id"] != user.id:
                referrals.insert_one({"referrer_id": referrer["_id"], "referred_id": user.id, "credited": False})

        # Force join check
        sub = await check_sub(client, user.id)
        if sub is not True:
            await message.reply("You must join the required channels to use this bot.", reply_markup=join_buttons())
            return

        # Send welcome image with caption
        try:
            await client.send_photo(
                chat_id=user.id,
                photo=START_IMAGE,      # URL or file_id of your welcome image
                caption=START_TEXT.format(first_name=user.first_name, username=user.username),
                reply_markup=main_keyboard()
            )
        except Exception as e:
            # fallback to text only if image fails
            await message.reply(
                START_TEXT.format(first_name=user.first_name, username=user.username),
                reply_markup=main_keyboard()
            )
