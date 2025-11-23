from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import SOURCE_CHANNELS

def main_keyboard():
    kb = [
        [InlineKeyboardButton("🎬 Categories", callback_data="menu_categories")],
        [InlineKeyboardButton("🔗 My Referral", callback_data="my_ref")],
        [InlineKeyboardButton("📊 My Status", callback_data="my_status")]
    ]
    return InlineKeyboardMarkup(kb)

def category_keyboard():
    kb = []
    for username, cat in SOURCE_CHANNELS.items():
        if not username:
            continue
        kb.append([InlineKeyboardButton(f"🎥 {cat.title()}", callback_data=f"cat_{cat}")])
    kb.append([InlineKeyboardButton("🔀 Random", callback_data="cat_random")])
    return InlineKeyboardMarkup(kb)

def join_buttons(channels):
    """Create join buttons dynamically."""
    kb = []
    for ch in channels:
        ch_username = ch.lstrip("@")
        kb.append([InlineKeyboardButton(f"Join {ch_username} ✅", url=f"https://t.me/{ch_username}")])
    kb.append([InlineKeyboardButton("I Joined ✅", callback_data="recheck_join")])
    return InlineKeyboardMarkup(kb)