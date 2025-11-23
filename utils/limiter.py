from datetime import datetime, timedelta
from database import users, watches
from config import DAILY_LIMIT, REFRESH_HOURS, REFERRAL_BONUS

def get_remaining(user_id):
    """
    Returns remaining videos, bonus, and already watched count
    """
    now = datetime.utcnow()
    cutoff = now - timedelta(hours=REFRESH_HOURS)
    watched_count = watches.count_documents({"user_id": user_id, "watched_at":{"$gte":cutoff}})
    user = users.find_one({"_id": user_id})
    bonus = user.get("bonus",0) if user else 0
    remaining = (DAILY_LIMIT - watched_count) + bonus
    return max(0, remaining), bonus, watched_count

def consume(user_id, video_id):
    """
    Consume one quota (bonus if available, otherwise normal daily limit)
    """
    user = users.find_one({"_id": user_id})
    if user and user.get("bonus",0) > 0:
        users.update_one({"_id": user_id}, {"$inc":{"bonus": -1}})
        return True, "bonus"
    remaining, bonus, watched_count = get_remaining(user_id)
    if remaining <= 0:
        return False, None
    watches.insert_one({"user_id": user_id, "video_id": video_id, "watched_at": datetime.utcnow()})
    return True, "normal"
