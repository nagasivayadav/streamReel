from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .database import engine, SessionLocal
from .routers import auth_routes, video_routes, watch_history_routes, recommendation_routes, profile_routes

# Creates tables if they don't exist. For real projects, use Alembic
# migrations instead of this once the schema stabilizes.
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="StreamReel API")

# In production, restrict allow_origins to your actual frontend domain.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_routes.router)
app.include_router(profile_routes.router)
app.include_router(video_routes.router)
app.include_router(watch_history_routes.router)
app.include_router(recommendation_routes.router)


@app.get("/")
def health_check():
    return {"status": "StreamReel backend is running"}


@app.get("/api/admin/reset-videos")
def reset_videos(key: str = ""):
    """
    Visit this URL directly in a browser to wipe the videos table and
    reseed it fresh from scripts/seed_videos.py. Requires a matching key
    so random visitors can't trigger it. Safe to call as many times as
    you like — it fully clears duplicates each time.
    """
    if key != "resetme123":
        return {"error": "Invalid key"}

    from scripts.seed_videos import seed, SAMPLE_VIDEOS

    db = SessionLocal()
    try:
        deleted = db.query(models.Video).delete()
        db.commit()
    finally:
        db.close()

    seed()

    return {
        "status": "reset complete",
        "deleted_old_rows": deleted,
        "reseeded_count": len(SAMPLE_VIDEOS),
    }