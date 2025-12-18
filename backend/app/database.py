from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from .config import get_settings

settings = get_settings()

# Default to SQLite for local development if Postgres URL not set
# In production/docker, we will set DATABASE_URL env var
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

# Fallback to SQLite if DATABASE_URL is not set (for safety/testing without real DB)
if "sqlite" in SQLALCHEMY_DATABASE_URL:
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, 
        connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
