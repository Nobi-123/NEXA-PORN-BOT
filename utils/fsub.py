from pyrogram.errors import UserNotParticipant

async def check_sub(client, user_id, channels):
    """
    Check if a user joined all mandatory channels.
    Returns True if joined all, False otherwise.
    """
    for ch in channels:
        try:
            member = await client.get_chat_member(ch, user_id)
            if member.status in ["kicked", "left"]:
                return False
        except UserNotParticipant:
            return False
        except Exception:
            return False
    return True