from datetime import datetime
from database import bot_logs
from config import LOG_CHANNEL

def log_event(text, app=None):
    """
    Logs events to MongoDB and optionally to LOG_CHANNEL
    """
    try:
        bot_logs.insert_one({"event": text, "ts": datetime.utcnow()})
    except Exception:
        pass
    if app and LOG_CHANNEL:
        try:
            app.send_message(LOG_CHANNEL, f"{datetime.utcnow().isoformat()} — {text}")
        except Exception:
            pass
