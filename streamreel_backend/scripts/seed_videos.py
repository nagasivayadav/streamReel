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
from urllib.parse import quote

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, engine, Base
from app import models


def poster_for(title, bg="1b1a20", fg="e8b84b"):
    """Builds a poster image with the movie title printed directly on it."""
    text = quote(title)
    return f"https://placehold.co/400x600/{bg}/{fg}?text={text}&font=roboto"


def backdrop_for(title, bg="0b0b0d", fg="f2f0ea"):
    """Builds a wide hero banner image with the movie title printed on it."""
    text = quote(title)
    return f"https://placehold.co/1280x720/{bg}/{fg}?text={text}&font=roboto"


SAMPLE_VIDEOS = [
    {"title": "Ridge Line", "genre": "Drama", "language": "English", "duration": 596,
     "hls_url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4",
     "is_featured": True},

    {"title": "Circuit Breakers", "genre": "Sci-Fi", "language": "English", "duration": 653,
     "hls_url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4",
     "is_featured": True},

    {"title": "Vaana Jallu", "genre": "Drama", "language": "Telugu", "duration": 734,
     "hls_url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4",
     "is_featured": True},

    {"title": "Prema Katha", "genre": "Comedy", "language": "Telugu", "duration": 15,
     "hls_url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerEscapes.mp4",
     "is_featured": False},

    {"title": "Dilse Dosti", "genre": "Drama", "language": "Hindi", "duration": 653,
     "hls_url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerFun.mp4",
     "is_featured": False},

    {"title": "Shehar Ki Raatein", "genre": "Thriller", "language": "Hindi", "duration": 734,
     "hls_url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerJoyrides.mp4",
     "is_featured": False},

    {"title": "Late Checkout", "genre": "Comedy", "language": "English", "duration": 15,
     "hls_url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerMeltdowns.mp4",
     "is_featured": False},

    {"title": "Nadi Oddu", "genre": "Documentary", "language": "Telugu", "duration": 596,
     "hls_url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/Sintel.mp4",
     "is_featured": False},

    {"title": "Yaadon Ka Safar", "genre": "Documentary", "language": "Hindi", "duration": 596,
     "hls_url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/SubaruOutbackOnStreetAndDirt.mp4",
     "is_featured": False},

    {"title": "Signal Loss", "genre": "Sci-Fi", "language": "English", "duration": 653,
     "hls_url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/TearsOfSteel.mp4",
     "is_featured": False},
]

# Fill in poster_url / backdrop_url for every entry automatically, so the
# title text is baked right into the image and always matches.
for v in SAMPLE_VIDEOS:
    v["poster_url"] = poster_for(v["title"])
    v["backdrop_url"] = backdrop_for(v["title"])


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