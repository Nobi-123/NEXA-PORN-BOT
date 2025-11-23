from datetime import datetime
from config import LOG_CHANNEL
from database import bot_logs

async def log_event(text, app=None):
    """Log to MongoDB and optionally LOG_CHANNEL"""
    try:
        bot_logs.insert_one({"event": text, "ts": datetime.utcnow()})
    except:
        pass

    if app and LOG_CHANNEL:
        try:
            await app.send_message(LOG_CHANNEL, f"{datetime.utcnow().isoformat()} — {text}")
        except:
            pass