import uuid
from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, TIMESTAMP, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

    profiles = relationship("Profile", back_populates="user", cascade="all, delete")


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    is_kids = Column(Boolean, default=False)

    user = relationship("User", back_populates="profiles")
    watch_history = relationship("WatchHistory", back_populates="profile", cascade="all, delete")


class Video(Base):
    __tablename__ = "videos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    genre = Column(String, index=True)
    language = Column(String, index=True, default="English")
    duration = Column(Integer)  # seconds
    hls_url = Column(String)   # path to the video file / manifest
    poster_url = Column(String)     # vertical/rectangle card image
    backdrop_url = Column(String)   # wide hero banner image
    is_featured = Column(Boolean, default=False)  # shows in the big hero banner


class WatchHistory(Base):
    __tablename__ = "watch_history"

    profile_id = Column(UUID(as_uuid=True), ForeignKey("profiles.id"), primary_key=True)
    video_id = Column(UUID(as_uuid=True), ForeignKey("videos.id"), primary_key=True)
    position_seconds = Column(Integer, default=0)
    last_watched_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    profile = relationship("Profile", back_populates="watch_history")
