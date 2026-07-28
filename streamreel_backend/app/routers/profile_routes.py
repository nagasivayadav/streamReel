from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import schemas
from .. import models
from ..database import get_db
from ..auth import decode_access_token

router = APIRouter(prefix="/api/profiles", tags=["profiles"])

MAX_PROFILES_PER_USER = 5


@router.post("", response_model=schemas.ProfileOut, status_code=status.HTTP_201_CREATED)
def create_profile(
    profile_in: schemas.ProfileCreate,
    db: Session = Depends(get_db),
    user_id: str = Depends(decode_access_token),
):
    existing_count = (
        db.query(models.Profile)
        .filter(models.Profile.user_id == user_id)
        .count()
    )
    if existing_count >= MAX_PROFILES_PER_USER:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Maximum of {MAX_PROFILES_PER_USER} profiles per account",
        )

    new_profile = models.Profile(
        user_id=user_id,
        name=profile_in.name,
        is_kids=profile_in.is_kids,
    )
    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)
    return new_profile


@router.get("", response_model=List[schemas.ProfileOut])
def list_profiles(
    db: Session = Depends(get_db),
    user_id: str = Depends(decode_access_token),
):
    return (
        db.query(models.Profile)
        .filter(models.Profile.user_id == user_id)
        .all()
    )


@router.delete("/{profile_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_profile(
    profile_id: str,
    db: Session = Depends(get_db),
    user_id: str = Depends(decode_access_token),
):
    profile = (
        db.query(models.Profile)
        .filter(models.Profile.id == profile_id, models.Profile.user_id == user_id)
        .first()
    )
    if not profile:
        # Ownership check baked into the query above — a user can't discover or
        # delete another account's profile by guessing IDs, and either "doesn't
        # exist" or "not yours" returns the same 404 so it can't be used to probe.
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")

    db.delete(profile)
    db.commit()
    return None
