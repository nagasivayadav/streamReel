"""
Populates the videos table with a 150-title catalog (50 English, 50 Hindi,
50 Telugu real movie names). Poster/backdrop images show the movie title
printed on a placeholder graphic — NOT official studio artwork, which is
copyrighted and can't be reproduced here. Swap poster_url/backdrop_url for
real licensed images whenever you have them.

Video playback cycles through a small pool of free, legal sample clips
(Google's public test-video bucket) since there isn't a free legal source
for 150 unique real film clips.

Usage:
    python -m scripts.seed_videos
Or inside docker:
    docker-compose exec backend python -m scripts.seed_videos
"""
import sys
import os
from urllib.parse import quote

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, engine, Base
from app import models


import requests

# Get a free key from https://www.themoviedb.org/settings/api and paste it here.
TMDB_API_KEY = "f518211c0ce9567e09ced7520d9cf823"
TMDB_IMAGE_BASE = "https://image.tmdb.org/t/p/w500"
TMDB_BACKDROP_BASE = "https://image.tmdb.org/t/p/w1280"

# Fallback used only if a title can't be found on TMDB or the API key is missing.
def _fallback_poster(title):
    text = quote(title)
    return f"https://placehold.co/400x600/1b1a20/e8b84b?text={text}&font=roboto"


def _fallback_backdrop(title):
    text = quote(title)
    return f"https://placehold.co/1280x720/0b0b0d/f2f0ea?text={text}&font=roboto"


_tmdb_cache = {}


def _tmdb_lookup(title):
    """Searches TMDB for a title and returns (poster_url, backdrop_url), or
    (None, None) if not found / API key not set / request fails."""
    if title in _tmdb_cache:
        return _tmdb_cache[title]

    if not TMDB_API_KEY or TMDB_API_KEY == "PASTE_YOUR_TMDB_API_KEY_HERE":
        return (None, None)

    try:
        resp = requests.get(
            "https://api.themoviedb.org/3/search/movie",
            params={"api_key": TMDB_API_KEY, "query": title},
            timeout=8,
        )
        results = resp.json().get("results", [])
        if not results:
            _tmdb_cache[title] = (None, None)
            return (None, None)

        best = results[0]
        poster = f"{TMDB_IMAGE_BASE}{best['poster_path']}" if best.get("poster_path") else None
        backdrop = f"{TMDB_BACKDROP_BASE}{best['backdrop_path']}" if best.get("backdrop_path") else None
        _tmdb_cache[title] = (poster, backdrop)
        return (poster, backdrop)
    except Exception as e:
        print(f"TMDB lookup failed for '{title}': {e}")
        return (None, None)


def poster_for(title):
    poster, _ = _tmdb_lookup(title)
    return poster or _fallback_poster(title)


def backdrop_for(title):
    _, backdrop = _tmdb_lookup(title)
    return backdrop or _fallback_backdrop(title)


VIDEO_POOL = [
    "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4",
    "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4",
    "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4",
    "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerEscapes.mp4",
    "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerFun.mp4",
    "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerJoyrides.mp4",
    "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerMeltdowns.mp4",
    "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/Sintel.mp4",
    "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/SubaruOutbackOnStreetAndDirt.mp4",
    "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/TearsOfSteel.mp4",
    "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/VolkswagenGTIReview.mp4",
    "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/WeAreGoingOnBullrun.mp4",
    "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/WhatCarCanYouGetForAGrand.mp4",
]

ENGLISH_TITLES = [
    ("Oppenheimer", "Drama"), ("Barbie", "Comedy"), ("Dune", "Sci-Fi"),
    ("Dune Part Two", "Sci-Fi"), ("Inside Out 2", "Adventure"),
    ("Deadpool and Wolverine", "Action"), ("Wicked", "Adventure"),
    ("Gladiator II", "Action"), ("Furiosa", "Action"),
    ("Godzilla x Kong", "Action"), ("Kingdom of the Planet of the Apes", "Adventure"),
    ("Twisters", "Action"), ("A Quiet Place Day One", "Horror"),
    ("Bad Boys Ride or Die", "Action"), ("Beetlejuice Beetlejuice", "Horror"),
    ("Joker Folie a Deux", "Drama"), ("Venom The Last Dance", "Action"),
    ("Moana 2", "Adventure"), ("Sonic the Hedgehog 3", "Adventure"),
    ("Mufasa The Lion King", "Adventure"), ("Alien Romulus", "Horror"),
    ("The Fall Guy", "Action"), ("Civil War", "Thriller"),
    ("Challengers", "Romance"), ("Anyone But You", "Romance"),
    ("Argylle", "Action"), ("The Marvels", "Action"),
    ("Aquaman and the Lost Kingdom", "Adventure"), ("Napoleon", "Drama"),
    ("The Hunger Games The Ballad of Songbirds and Snakes", "Adventure"),
    ("Wonka", "Comedy"), ("Migration", "Adventure"), ("Mean Girls", "Comedy"),
    ("The Beekeeper", "Action"), ("Madame Web", "Action"),
    ("Kung Fu Panda 4", "Adventure"), ("Ghostbusters Frozen Empire", "Horror"),
    ("Monkey Man", "Action"), ("Abigail", "Horror"), ("IF", "Comedy"),
    ("The Garfield Movie", "Comedy"), ("Longlegs", "Horror"), ("Trap", "Thriller"),
    ("Blink Twice", "Thriller"), ("Speak No Evil", "Horror"),
    ("Terrifier 3", "Horror"), ("Smile 2", "Horror"), ("Nosferatu", "Horror"),
    ("Wolf Man", "Horror"), ("Sinners", "Horror"),
    ("Indiana Jones and the Dial of Destiny", "Adventure"),
    ("Jumanji The Next Level", "Adventure"),
    ("Mission Impossible The Final Reckoning", "Action"),
    ("Talk to Me", "Horror"), ("M3GAN 2.0", "Horror"),
    ("It Ends With Us", "Romance"),
]

HINDI_TITLES = [
    ("Animal", "Action"), ("Jawan", "Action"), ("Pathaan", "Action"),
    ("Gadar 2", "Action"), ("Rocky Aur Rani Kii Prem Kahaani", "Romance"),
    ("12th Fail", "Drama"), ("Sam Bahadur", "Drama"), ("Dunki", "Comedy"),
    ("Fighter", "Action"), ("Crew", "Comedy"), ("Madgaon Express", "Comedy"),
    ("Article 370", "Drama"), ("Shaitaan", "Horror"),
    ("Bade Miyan Chote Miyan", "Action"), ("Maidaan", "Drama"),
    ("Amar Singh Chamkila", "Drama"), ("Munjya", "Horror"),
    ("Chandu Champion", "Drama"), ("Auron Mein Kahan Dum Tha", "Drama"),
    ("Stree 2", "Horror"), ("Khel Khel Mein", "Comedy"), ("Vedaa", "Action"),
    ("Jigra", "Drama"), ("Singham Again", "Action"),
    ("Bhool Bhulaiyaa 3", "Horror"), ("Baby John", "Action"),
    ("Sky Force", "Action"), ("Deva", "Action"), ("Loveyapa", "Romance"),
    ("Chhaava", "Action"), ("Sikandar", "Action"), ("Housefull 5", "Comedy"),
    ("Metro In Dino", "Romance"), ("Raid 2", "Action"), ("Jaat", "Action"),
    ("Kesari Chapter 2", "Drama"), ("Sitaare Zameen Par", "Comedy"),
    ("Saiyaara", "Romance"), ("Dhurandhar", "Action"), ("Border 2", "Action"),
    ("De De Pyaar De 2", "Romance"), ("War 2", "Action"), ("Alpha", "Action"),
    ("Thug Life", "Action"), ("Welcome to the Jungle", "Adventure"),
    ("Coolie", "Action"), ("Bhagwant Kesari", "Action"),
    ("Son of Sardaar 2", "Comedy"), ("Kaagaz 2", "Drama"),
    ("Vicky Vidya Ka Woh Wala Video", "Comedy"),
]

TELUGU_TITLES = [
    ("Salaar", "Action"), ("Kalki 2898 AD", "Adventure"),
    ("Guntur Kaaram", "Action"), ("Hi Nanna", "Drama"), ("Eagle", "Action"),
    ("Family Star", "Romance"), ("Manamey", "Romance"),
    ("Om Bheem Bush", "Comedy"), ("Aadikeshava", "Action"),
    ("Tillu Square", "Comedy"), ("Vishwambhara", "Action"),
    ("Devara", "Action"), ("Lucky Baskhar", "Drama"),
    ("Pushpa 2 The Rule", "Action"), ("Naa Saami Ranga", "Action"),
    ("Committee Kurrollu", "Comedy"), ("Mechanic Rocky", "Action"),
    ("Gandeevadhari Arjuna", "Action"), ("Bhairavam", "Action"),
    ("Sarangapani Jathakam", "Comedy"), ("Cinema Bandi", "Comedy"),
    ("Custody", "Action"), ("Double iSmart", "Action"), ("Gaami", "Thriller"),
    ("Rules Ranjann", "Romance"), ("HanuMan", "Adventure"),
    ("Baby", "Romance"), ("Balagam", "Drama"), ("Bhaje Vaayu Vegam", "Comedy"),
    ("Kushi", "Romance"), ("Skanda", "Action"), ("Bro", "Comedy"),
    ("Waltair Veerayya", "Action"), ("Veera Simha Reddy", "Action"),
    ("Dasara", "Drama"), ("Virupaksha", "Horror"),
    ("Miss Shetty Mr Polishetty", "Comedy"), ("Sridevi Soda Center", "Romance"),
    ("Ambajipeta Marriage Band", "Drama"), ("Vaathi", "Drama"),
    ("Mad", "Comedy"), ("Samajavaragamana", "Comedy"),
    ("Mangalavaaram", "Horror"), ("Saindhav", "Action"),
    ("Music School", "Drama"), ("Buddy", "Action"),
    ("Sarkaru Vaari Paata", "Action"), ("Konda Polam", "Drama"),
    ("Most Eligible Bachelor", "Romance"), ("Bangarraju", "Comedy"),
]


def build_catalog():
    catalog = []
    all_titles = (
        [(t, g, "English") for t, g in ENGLISH_TITLES]
        + [(t, g, "Hindi") for t, g in HINDI_TITLES]
        + [(t, g, "Telugu") for t, g in TELUGU_TITLES]
    )
    for i, (title, genre, language) in enumerate(all_titles):
        catalog.append({
            "title": title,
            "genre": genre,
            "language": language,
            "duration": 6000 + (i % 5) * 300,
            "hls_url": VIDEO_POOL[i % len(VIDEO_POOL)],
            "poster_url": poster_for(title),
            "backdrop_url": backdrop_for(title),
            "is_featured": (i % 15 == 0),
        })
    return catalog


SAMPLE_VIDEOS = build_catalog()


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