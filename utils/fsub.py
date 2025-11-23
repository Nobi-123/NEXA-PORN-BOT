from pyrogram.errors import UserNotParticipant, BadRequest
from config import FORCE_CHANNELS

async def check_sub(client, user_id):
    """
    Checks if the user has joined all required channels
    Returns True if joined, otherwise returns the channel they haven't joined
    """
    for ch in FORCE_CHANNELS:
        if not ch:
            continue
        try:
            mem = await client.get_chat_member(int(ch), user_id)
            if mem.status in ("kicked",):
                return ch
        except UserNotParticipant:
            return ch
        except BadRequest:
            return ch
        except Exception:
            return ch
    return True
