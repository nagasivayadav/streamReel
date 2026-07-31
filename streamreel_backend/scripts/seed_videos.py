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


def poster_for(title):
    text = quote(title)
    return f"https://placehold.co/400x600/1b1a20/e8b84b?text={text}&font=roboto"


def backdrop_for(title):
    text = quote(title)
    return f"https://placehold.co/1280x720/0b0b0d/f2f0ea?text={text}&font=roboto"


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

GENRES = ["Drama", "Action", "Comedy", "Thriller", "Romance"]

ENGLISH_TITLES = [
    "Oppenheimer", "Barbie", "Dune", "Dune Part Two", "Inside Out 2",
    "Deadpool and Wolverine", "Wicked", "Gladiator II", "Furiosa",
    "Godzilla x Kong", "Kingdom of the Planet of the Apes", "Twisters",
    "A Quiet Place Day One", "Bad Boys Ride or Die", "Beetlejuice Beetlejuice",
    "Joker Folie a Deux", "Venom The Last Dance", "Moana 2",
    "Sonic the Hedgehog 3", "Mufasa The Lion King", "Alien Romulus",
    "The Fall Guy", "Civil War", "Challengers", "Anyone But You", "Argylle",
    "The Marvels", "Aquaman and the Lost Kingdom", "Napoleon",
    "The Hunger Games The Ballad of Songbirds and Snakes", "Wonka",
    "Migration", "Mean Girls", "The Beekeeper", "Madame Web",
    "Kung Fu Panda 4", "Ghostbusters Frozen Empire", "Monkey Man", "Abigail",
    "IF", "The Garfield Movie", "Longlegs", "Trap", "Blink Twice",
    "Speak No Evil", "Terrifier 3", "Smile 2", "Nosferatu", "Wolf Man",
    "Sinners",
]

HINDI_TITLES = [
    "Animal", "Jawan", "Pathaan", "Gadar 2", "Rocky Aur Rani Kii Prem Kahaani",
    "12th Fail", "Sam Bahadur", "Dunki", "Fighter", "Crew",
    "Madgaon Express", "Article 370", "Shaitaan", "Bade Miyan Chote Miyan",
    "Maidaan", "Amar Singh Chamkila", "Munjya", "Chandu Champion",
    "Auron Mein Kahan Dum Tha", "Stree 2", "Khel Khel Mein", "Vedaa",
    "Jigra", "Singham Again", "Bhool Bhulaiyaa 3", "Baby John", "Sky Force",
    "Deva", "Loveyapa", "Chhaava", "Sikandar", "Housefull 5", "Metro In Dino",
    "Raid 2", "Jaat", "Kesari Chapter 2", "Sitaare Zameen Par", "Saiyaara",
    "Dhurandhar", "Border 2", "De De Pyaar De 2", "War 2", "Alpha",
    "Thug Life", "Welcome to the Jungle", "Coolie", "Bhagwant Kesari",
    "Son of Sardaar 2", "Kaagaz 2", "Vicky Vidya Ka Woh Wala Video",
]

TELUGU_TITLES = [
    "Salaar", "Kalki 2898 AD", "Guntur Kaaram", "Hi Nanna", "Eagle",
    "Family Star", "Manamey", "Om Bheem Bush", "Aadikeshava", "Tillu Square",
    "Vishwambhara", "Devara", "Lucky Baskhar", "Pushpa 2 The Rule",
    "Naa Saami Ranga", "Committee Kurrollu", "Mechanic Rocky",
    "Gandeevadhari Arjuna", "Bhairavam", "Sarangapani Jathakam",
    "Cinema Bandi", "Custody", "Double iSmart", "Gaami", "Rules Ranjann",
    "HanuMan", "Baby", "Balagam", "Bhaje Vaayu Vegam", "Kushi", "Skanda",
    "Bro", "Waltair Veerayya", "Veera Simha Reddy", "Dasara", "Virupaksha",
    "Miss Shetty Mr Polishetty", "Sridevi Soda Center",
    "Ambajipeta Marriage Band", "Vaathi", "Mad", "Samajavaragamana",
    "Mangalavaaram", "Saindhav", "Music School", "Buddy",
    "Sarkaru Vaari Paata", "Konda Polam", "Most Eligible Bachelor",
    "Bangarraju",
]


def build_catalog():
    catalog = []
    all_titles = (
        [(t, "English") for t in ENGLISH_TITLES]
        + [(t, "Hindi") for t in HINDI_TITLES]
        + [(t, "Telugu") for t in TELUGU_TITLES]
    )
    for i, (title, language) in enumerate(all_titles):
        catalog.append({
            "title": title,
            "genre": GENRES[i % len(GENRES)],
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