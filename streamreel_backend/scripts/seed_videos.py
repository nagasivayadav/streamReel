"""
Populates the videos table with sample catalog data so the app isn't empty
on first run. Safe to re-run — skips titles that already exist instead of
creating duplicates.

Usage (from the backend project root, with DATABASE_URL pointing at your DB):
    python -m scripts.seed_videos

Or inside the running docker container:
    docker-compose exec backend python -m scripts.seed_videos
"""
import sys
import os

# Allow running this file directly (`python scripts/seed_videos.py`) as well
# as as a module (`python -m scripts.seed_videos`).
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, engine, Base
from app import models

SAMPLE_VIDEOS = [
    {"title": "Ridge Line", "genre": "Drama", "duration": 6420, "hls_url": "/media/ridge-line/master.m3u8"},
    {"title": "Circuit Breakers", "genre": "Sci-Fi", "duration": 5580, "hls_url": "/media/circuit-breakers/master.m3u8"},
    {"title": "Late Checkout", "genre": "Comedy", "duration": 4980, "hls_url": "/media/late-checkout/master.m3u8"},
    {"title": "The Long Ferry", "genre": "Thriller", "duration": 7140, "hls_url": "/media/long-ferry/master.m3u8"},
    {"title": "Paper Moons", "genre": "Documentary", "duration": 3600, "hls_url": "/media/paper-moons/master.m3u8"},
    {"title": "Signal Loss", "genre": "Sci-Fi", "duration": 6000, "hls_url": "/media/signal-loss/master.m3u8"},
    {"title": "Kitchen Table Wars", "genre": "Comedy", "duration": 5400, "hls_url": "/media/kitchen-table-wars/master.m3u8"},
    {"title": "Northbound", "genre": "Drama", "duration": 6900, "hls_url": "/media/northbound/master.m3u8"},
    {"title": "Small Hours", "genre": "Thriller", "duration": 5760, "hls_url": "/media/small-hours/master.m3u8"},
    {"title": "The Cartographer", "genre": "Documentary", "duration": 4200, "hls_url": "/media/the-cartographer/master.m3u8"},
    {"title": "Glasshouse", "genre": "Drama", "duration": 6300, "hls_url": "/media/glasshouse/master.m3u8"},
    {"title": "Static Bloom", "genre": "Sci-Fi", "duration": 5940, "hls_url": "/media/static-bloom/master.m3u8"},
    {"title": "Ridge Line", "genre": "Drama", "language": "English", "duration": 596, "hls_url": "https://interactive-examples.mdn.mozilla.net/media/cc0-videos/flower.mp4"},
    {"title": "Circuit Breakers", "genre": "Sci-Fi", "language": "English", "duration": 653, "hls_url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4"},
    {"title": "Vaana Jallu", "genre": "Drama", "language": "Telugu", "duration": 734, "hls_url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4"},
    {"title": "Prema Katha", "genre": "Comedy", "language": "Telugu", "duration": 15, "hls_url": "https://interactive-examples.mdn.mozilla.net/media/cc0-videos/friday.mp4"},
    {"title": "Dilse Dosti", "genre": "Drama", "language": "Hindi", "duration": 653, "hls_url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4"},
    {"title": "Shehar Ki Raatein", "genre": "Thriller", "language": "Hindi", "duration": 734, "hls_url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4"},
    {"title": "Late Checkout", "genre": "Comedy", "language": "English", "duration": 15, "hls_url": "https://interactive-examples.mdn.mozilla.net/media/cc0-videos/friday.mp4"},
    {"title": "Nadi ఒడ్డున", "genre": "Documentary", "language": "Telugu", "duration": 596, "hls_url": "https://interactive-examples.mdn.mozilla.net/media/cc0-videos/flower.mp4"},
    {"title": "Yaadon Ka Safar", "genre": "Documentary", "language": "Hindi", "duration": 596, "hls_url": "https://interactive-examples.mdn.mozilla.net/media/cc0-videos/flower.mp4"},
    {"title": "Signal Loss", "genre": "Sci-Fi", "language": "English", "duration": 653, "hls_url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4"},
]

def seed():
    # Make sure tables exist — mirrors what main.py does on startup, so this
    # script works even against a completely fresh database.
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        existing_titles = {
            title for (title,) in db.query(models.Video.title).all()
        }

        created = 0
        for video_data in SAMPLE_VIDEOS:
            if video_data["title"] in existing_titles:
                continue
            db.add(models.Video(**video_data))
            created += 1

        db.commit()
        print(f"Seed complete: {created} video(s) added, {len(SAMPLE_VIDEOS) - created} already existed.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
