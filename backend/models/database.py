"""
Database connection setup for the RAG Chatbot with Neon Postgres
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from ..config.settings import settings
import logging

logger = logging.getLogger(__name__)

# Create database engine for Neon Postgres
engine = create_engine(
    settings.neon_database_url,
    echo=settings.db_echo,  # Set to True to log SQL queries
    pool_pre_ping=True,  # Ensures connections are valid
    pool_recycle=300,   # Recycle connections every 5 minutes
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all models
Base = declarative_base()

def get_db():
    """
    Dependency to get database session
    """
    db = SessionLocal()
    try:
        logger.debug("Database session created")
        yield db
    finally:
        db.close()
        logger.debug("Database session closed")