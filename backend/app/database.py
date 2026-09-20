import os
import logging
from dotenv import load_dotenv, find_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv(find_dotenv())

logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+pg8000://postgres:3131@localhost:5432/devils_advocate"
)

# Use pg8000 driver for PostgreSQL if no specific driver is given
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+pg8000://", 1)
elif DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+pg8000://", 1)

# Default to SQLite fallback if Postgres is unreachable
sqlite_db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "devils_advocate.db")
SQLITE_URL = f"sqlite:///{sqlite_db_path}"

try:
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)
    # Quick probe
    with engine.connect() as conn:
        logger.debug("Database probe connection verified")
    logger.info("Successfully connected to PostgreSQL database")
except Exception as e:
    logger.warning(f"PostgreSQL connection failed ({e}); falling back to persistent SQLite at {sqlite_db_path}")
    engine = create_engine(SQLITE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initializes all database tables to guarantee session persistence."""
    try:
        from . import models  # noqa
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables initialized successfully")
    except Exception as e:
        logger.warning(f"init_db notice: {e}")
