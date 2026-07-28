from collections import Counter
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import schemas
from .. import models
from ..database import get_db
from ..auth import decode_access_token

router = APIRouter(prefix="/api/recommendations", tags=["recommendations"])


@router.get("/{profile_id}", response_model=list[schemas.VideoOut])
def get_recommendations(
    profile_id: str,
    db: Session = Depends(get_db),
    user_id: str = Depends(decode_access_token),
):
    """
    Minimal content-based recommender:
    1. Look at what genres this profile has actually watched.
    2. Recommend other videos in those genres that haven't been watched yet.

    This is intentionally simple so it's easy to defend in a viva —
    swap this function out for collaborative filtering (e.g. using
    pandas/scikit-learn cosine similarity across all profiles' watch
    vectors) once you want a stronger version.
    """
    watched = (
        db.query(models.WatchHistory)
        .filter(models.WatchHistory.profile_id == profile_id)
        .all()
    )
    watched_video_ids = [w.video_id for w in watched]

    if not watched_video_ids:
        # Cold start: no history yet, just return trending/catalog videos.
        return db.query(models.Video).limit(10).all()

    watched_videos = (
        db.query(models.Video).filter(models.Video.id.in_(watched_video_ids)).all()
    )
    genre_counts = Counter(v.genre for v in watched_videos if v.genre)
    top_genres = [genre for genre, _ in genre_counts.most_common(3)]

    recommendations = (
        db.query(models.Video)
        .filter(models.Video.genre.in_(top_genres))
        .filter(models.Video.id.notin_(watched_video_ids))
        .limit(10)
        .all()
    )
    return recommendations
