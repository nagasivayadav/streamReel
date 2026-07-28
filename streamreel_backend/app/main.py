from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .database import engine
from .routers import auth_routes, video_routes, watch_history_routes, recommendation_routes, profile_routes

# Creates tables if they don't exist. For real projects, use Alembic
# migrations instead of this once the schema stabilizes.
models.Base.metadata.create_all(bind=engine)

# Auto-seed sample videos on startup (needed since the free Render plan
# doesn't include Shell access to run the seed script manually).
from scripts.seed_videos import seed
seed()

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