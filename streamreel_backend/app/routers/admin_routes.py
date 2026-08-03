import uuid
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

from .. import models
from ..database import SessionLocal

router = APIRouter(prefix="/api/admin", tags=["admin"])

# Simple shared-secret key so random visitors can't add/delete your catalog.
# Change this to something only you know, and don't share it publicly.
ADMIN_KEY = "resetme123"


def check_key(key: str):
    if key != ADMIN_KEY:
        raise HTTPException(status_code=403, detail="Invalid admin key")


class VideoIn(BaseModel):
    title: str
    genre: Optional[str] = None
    language: Optional[str] = "English"
    duration: Optional[int] = 0
    hls_url: Optional[str] = None
    poster_url: Optional[str] = None
    backdrop_url: Optional[str] = None
    is_featured: Optional[bool] = False


@router.get("/videos")
def admin_list_videos(key: str = ""):
    check_key(key)
    db = SessionLocal()
    try:
        videos = db.query(models.Video).order_by(models.Video.title).all()
        return [
            {
                "id": str(v.id), "title": v.title, "genre": v.genre,
                "language": v.language, "duration": v.duration,
                "hls_url": v.hls_url, "poster_url": v.poster_url,
                "backdrop_url": v.backdrop_url, "is_featured": v.is_featured,
            }
            for v in videos
        ]
    finally:
        db.close()


@router.post("/videos")
def admin_add_video(video: VideoIn, key: str = ""):
    check_key(key)
    db = SessionLocal()
    try:
        new_video = models.Video(**video.dict())
        db.add(new_video)
        db.commit()
        return {"status": "added", "id": str(new_video.id)}
    finally:
        db.close()


@router.put("/videos/{video_id}")
def admin_update_video(video_id: uuid.UUID, video: VideoIn, key: str = ""):
    check_key(key)
    db = SessionLocal()
    try:
        existing = db.query(models.Video).filter(models.Video.id == video_id).first()
        if not existing:
            raise HTTPException(status_code=404, detail="Video not found")
        for field, value in video.dict().items():
            setattr(existing, field, value)
        db.commit()
        return {"status": "updated"}
    finally:
        db.close()


@router.delete("/videos/{video_id}")
def admin_delete_video(video_id: uuid.UUID, key: str = ""):
    check_key(key)
    db = SessionLocal()
    try:
        existing = db.query(models.Video).filter(models.Video.id == video_id).first()
        if not existing:
            raise HTTPException(status_code=404, detail="Video not found")
        db.delete(existing)
        db.commit()
        return {"status": "deleted"}
    finally:
        db.close()