import uuid
from pydantic import BaseModel, EmailStr
from typing import Optional


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class ProfileCreate(BaseModel):
    name: str
    is_kids: bool = False


class ProfileOut(BaseModel):
    id: uuid.UUID
    name: str
    is_kids: bool

    class Config:
        orm_mode = True


class VideoOut(BaseModel):
    id: uuid.UUID
    title: str
    genre: Optional[str]
    language: Optional[str]
    duration: Optional[int]
    hls_url: Optional[str]
    poster_url: Optional[str]
    backdrop_url: Optional[str]
    is_featured: Optional[bool]

    class Config:
        orm_mode = True


class WatchHistoryUpdate(BaseModel):
    profile_id: uuid.UUID
    video_id: uuid.UUID
    position_seconds: int
