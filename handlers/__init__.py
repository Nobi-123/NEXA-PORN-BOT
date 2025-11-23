from .start import register_start
from .video_handlers import register_video
from .admin import register_admin
from .scraper_handler import register_scraper

def register_handlers(app):
    register_start(app)
    register_video(app)
    register_admin(app)
    register_scraper(app)
