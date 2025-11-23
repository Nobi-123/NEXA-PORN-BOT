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
    for code, cat in SOURCE_CHANNELS.items():
        if not code:
            continue
        kb.append([InlineKeyboardButton(f"🎥 {cat.title()}", callback_data=f"cat_{cat}")])
    kb.append([InlineKeyboardButton("🔀 Random", callback_data="cat_random")])
    return InlineKeyboardMarkup(kb)

def join_buttons():
    kb = []
    for ch in SOURCE_CHANNELS.keys():
        if not ch:
            continue
        kb.append([InlineKeyboardButton("Join Channel ✅", url=f"https://t.me/{ch}")])
    kb.append([InlineKeyboardButton("I Joined ✅", callback_data="recheck_join")])
    return InlineKeyboardMarkup(kb)
