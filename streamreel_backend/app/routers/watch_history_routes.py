from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/api/watch-history", tags=["watch-history"])


@router.post("")
def save_watch_position(payload: schemas.WatchHistoryUpdate, db: Session = Depends(get_db)):
    entry = db.query(models.WatchHistory).filter(
        models.WatchHistory.profile_id == payload.profile_id,
        models.WatchHistory.video_id == payload.video_id,
    ).first()

    if entry:
        entry.position_seconds = payload.position_seconds
    else:
        entry = models.WatchHistory(
            profile_id=payload.profile_id,
            video_id=payload.video_id,
            position_seconds=payload.position_seconds,
        )
        db.add(entry)

    db.commit()
    return {"detail": "Watch position saved"}


@router.get("/{profile_id}/{video_id}")
def get_resume_position(profile_id: uuid.UUID, video_id: uuid.UUID, db: Session = Depends(get_db)):
    entry = db.query(models.WatchHistory).filter(
        models.WatchHistory.profile_id == profile_id,
        models.WatchHistory.video_id == video_id,
    ).first()
    if not entry:
        return {"position_seconds": 0}
    return {"position_seconds": entry.position_seconds}


@router.get("/{profile_id}", response_model=list[schemas.VideoOut])
def list_watch_history(profile_id: uuid.UUID, db: Session = Depends(get_db)):
    """
    Returns the videos a profile has watched, most recent first — powers
    the "Continue Watching" row on the Browse page.
    """
    entries = (
        db.query(models.WatchHistory)
        .filter(models.WatchHistory.profile_id == profile_id)
        .order_by(models.WatchHistory.last_watched_at.desc())
        .limit(20)
        .all()
    )
    video_ids = [e.video_id for e in entries]
    if not video_ids:
        return []

    videos_by_id = {
        v.id: v for v in db.query(models.Video).filter(models.Video.id.in_(video_ids)).all()
    }
    # Preserve the most-recent-first order from watch history
    return [videos_by_id[vid] for vid in video_ids if vid in videos_by_id]