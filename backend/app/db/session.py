"""
Database Session and Engine Management
CSIR Healthcare Clinical Decision Support System (CDSS/DDSS)
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.app.db.models import Base

# Default to SQLite local database for development / test when PostgreSQL is not configured
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./cdss_local.db")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """Create local tables if they do not exist."""
    Base.metadata.create_all(bind=engine)


def get_db():
    """FastAPI dependency for database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
