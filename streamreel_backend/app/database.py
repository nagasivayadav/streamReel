import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Set this via environment variable in production. Example:
# postgresql://username:password@localhost:5432/streamreel
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/streamreel")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """Dependency used by every route that needs database access."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
