from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/api/videos", tags=["videos"])


@router.get("", response_model=list[schemas.VideoOut])
def list_videos(genre: str | None = None, language: str | None = None, db: Session = Depends(get_db)):
    query = db.query(models.Video)
    if genre:
        query = query.filter(models.Video.genre == genre)
    if language:
        query = query.filter(models.Video.language == language)
    return query.all()


@router.get("/featured", response_model=list[schemas.VideoOut])
def list_featured(db: Session = Depends(get_db)):
    """Videos marked as is_featured=True, shown in the big hero banner."""
    return db.query(models.Video).filter(models.Video.is_featured == True).all()  # noqa: E712


@router.get("/search", response_model=list[schemas.VideoOut])
def search_videos(q: str, db: Session = Depends(get_db)):
    return db.query(models.Video).filter(models.Video.title.ilike(f"%{q}%")).all()


@router.get("/{video_id}", response_model=schemas.VideoOut)
def get_video(video_id: uuid.UUID, db: Session = Depends(get_db)):
    video = db.query(models.Video).filter(models.Video.id == video_id).first()
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    return video
