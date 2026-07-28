from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .database import engine
from .routers import watch_history_routes
from .routers import auth_routes
from .routers import profile_routes
from .routers import recommendation_routes
from .routers import video_routes

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
