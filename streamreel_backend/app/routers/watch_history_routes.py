from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import schemas
from .. import models
from ..database import get_db
from ..auth import decode_access_token

router = APIRouter(prefix="/api/watch-history", tags=["watch-history"])


@router.post("")
def update_watch_history(
    entry: schemas.WatchHistoryUpdate,
    db: Session = Depends(get_db),
    user_id: str = Depends(decode_access_token),
):
    record = (
        db.query(models.WatchHistory)
        .filter(
            models.WatchHistory.profile_id == entry.profile_id,
            models.WatchHistory.video_id == entry.video_id,
        )
        .first()
    )
    if record:
        record.position_seconds = entry.position_seconds
    else:
        record = models.WatchHistory(**entry.dict())
        db.add(record)

    db.commit()
    return {"status": "saved", "position_seconds": entry.position_seconds}


@router.get("/{profile_id}/{video_id}")
def get_resume_position(
    profile_id: str,
    video_id: str,
    db: Session = Depends(get_db),
    user_id: str = Depends(decode_access_token),
):
    record = (
        db.query(models.WatchHistory)
        .filter(
            models.WatchHistory.profile_id == profile_id,
            models.WatchHistory.video_id == video_id,
        )
        .first()
    )
    if not record:
        return {"position_seconds": 0}
    return {"position_seconds": record.position_seconds}
