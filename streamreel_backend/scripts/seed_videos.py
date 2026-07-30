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

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, engine, Base
from app import models

# Poster = upright card image (2:3 ratio look), Backdrop = wide hero banner image.
# Using picsum.photos placeholder images (free, no login, no copyright issue) —
# swap these for real artwork whenever you have it.
SAMPLE_VIDEOS = [
    {"title": "Ridge Line", "genre": "Drama", "language": "English", "duration": 596,
     "hls_url": "https://interactive-examples.mdn.mozilla.net/media/cc0-videos/flower.mp4",
     "poster_url": "https://picsum.photos/seed/ridgeline/400/600",
     "backdrop_url": "https://picsum.photos/seed/ridgeline/1280/720",
     "is_featured": True},

    {"title": "Circuit Breakers", "genre": "Sci-Fi", "language": "English", "duration": 653,
     "hls_url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4",
     "poster_url": "https://picsum.photos/seed/circuitbreakers/400/600",
     "backdrop_url": "https://picsum.photos/seed/circuitbreakers/1280/720",
     "is_featured": True},

    {"title": "Vaana Jallu", "genre": "Drama", "language": "Telugu", "duration": 734,
     "hls_url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4",
     "poster_url": "https://picsum.photos/seed/vaanajallu/400/600",
     "backdrop_url": "https://picsum.photos/seed/vaanajallu/1280/720",
     "is_featured": True},

    {"title": "Prema Katha", "genre": "Comedy", "language": "Telugu", "duration": 15,
     "hls_url": "https://interactive-examples.mdn.mozilla.net/media/cc0-videos/friday.mp4",
     "poster_url": "https://picsum.photos/seed/premakatha/400/600",
     "backdrop_url": "https://picsum.photos/seed/premakatha/1280/720",
     "is_featured": False},

    {"title": "Dilse Dosti", "genre": "Drama", "language": "Hindi", "duration": 653,
     "hls_url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4",
     "poster_url": "https://picsum.photos/seed/dilsedosti/400/600",
     "backdrop_url": "https://picsum.photos/seed/dilsedosti/1280/720",
     "is_featured": False},

    {"title": "Shehar Ki Raatein", "genre": "Thriller", "language": "Hindi", "duration": 734,
     "hls_url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4",
     "poster_url": "https://picsum.photos/seed/sheharkiraatein/400/600",
     "backdrop_url": "https://picsum.photos/seed/sheharkiraatein/1280/720",
     "is_featured": False},

    {"title": "Late Checkout", "genre": "Comedy", "language": "English", "duration": 15,
     "hls_url": "https://interactive-examples.mdn.mozilla.net/media/cc0-videos/friday.mp4",
     "poster_url": "https://picsum.photos/seed/latecheckout/400/600",
     "backdrop_url": "https://picsum.photos/seed/latecheckout/1280/720",
     "is_featured": False},

    {"title": "Nadi Oddu", "genre": "Documentary", "language": "Telugu", "duration": 596,
     "hls_url": "https://interactive-examples.mdn.mozilla.net/media/cc0-videos/flower.mp4",
     "poster_url": "https://picsum.photos/seed/nadioddu/400/600",
     "backdrop_url": "https://picsum.photos/seed/nadioddu/1280/720",
     "is_featured": False},

    {"title": "Yaadon Ka Safar", "genre": "Documentary", "language": "Hindi", "duration": 596,
     "hls_url": "https://interactive-examples.mdn.mozilla.net/media/cc0-videos/flower.mp4",
     "poster_url": "https://picsum.photos/seed/yaadonkasafar/400/600",
     "backdrop_url": "https://picsum.photos/seed/yaadonkasafar/1280/720",
     "is_featured": False},

    {"title": "Signal Loss", "genre": "Sci-Fi", "language": "English", "duration": 653,
     "hls_url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4",
     "poster_url": "https://picsum.photos/seed/signalloss/400/600",
     "backdrop_url": "https://picsum.photos/seed/signalloss/1280/720",
     "is_featured": False},
]


def seed():
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