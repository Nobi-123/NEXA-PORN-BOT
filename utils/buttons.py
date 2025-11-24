from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import SOURCE_CHANNELS


# Main Menu Keyboard
def main_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🎬 Categories", callback_data="menu_categories")],
        [InlineKeyboardButton("🔗 My Referral", callback_data="my_ref")],
        [InlineKeyboardButton("📊 My Status", callback_data="my_status")]
    ])


# Category Keyboard (Auto from SOURCE_CHANNELS)
def category_keyboard():
    kb = []

    for username, cat in SOURCE_CHANNELS.items():
        if not username or not cat:
            continue

        kb.append([
            InlineKeyboardButton(
                f"🎥 {cat.title()}",
                callback_data=f"cat_{cat}"
            )
        ])

    # Random option
    kb.append([InlineKeyboardButton("🔀 Random", callback_data="cat_random")])

    return InlineKeyboardMarkup(kb)


# Dynamic Join Buttons
def join_buttons(channels: list):
    """
    channels: list of channels → ["@abc", "@xyz"]
    """
    kb = []

    for ch in channels:
        if not ch:
            continue

        ch_username = ch.replace("@", "").strip()

        kb.append([
            InlineKeyboardButton(
                f"Join @{ch_username} ✅",
                url=f"https://t.me/{ch_username}"
            )
        ])

    # Recheck Button
    kb.append([
        InlineKeyboardButton("I Joined ✅", callback_data="recheck_join")
    ])

    return InlineKeyboardMarkup(kb)