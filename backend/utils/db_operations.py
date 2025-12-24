"""
Database operations for the RAG Chatbot
"""
from sqlalchemy.orm import Session
from typing import Optional
from models import models, schemas
from uuid import UUID
import uuid


# Session operations
def create_session(db: Session, session: schemas.ChatSessionCreate) -> models.ChatSession:
    """Create a new chat session in the database"""
    db_session = models.ChatSession(
        user_id=session.user_id,
        metadata=session.metadata,
        is_active=True
    )
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session


def get_session(db: Session, session_id: str) -> Optional[models.ChatSession]:
    """Retrieve a chat session by ID"""
    session_uuid = UUID(session_id)
    return db.query(models.ChatSession).filter(models.ChatSession.session_id == session_uuid).first()


# Query operations
def create_query(db: Session, query: schemas.QueryCreate) -> models.Query:
    """Create a new query in the database"""
    db_query = models.Query(
        session_id=UUID(query.session_id),
        query_text=query.query_text,
        query_mode=query.query_mode,
        selected_text=query.selected_text,
        source_reference=query.source_reference
    )
    db.add(db_query)
    db.commit()
    db.refresh(db_query)
    return db_query


def get_query(db: Session, query_id: str) -> Optional[models.Query]:
    """Retrieve a query by ID"""
    query_uuid = UUID(query_id)
    return db.query(models.Query).filter(models.Query.query_id == query_uuid).first()


# Response operations
def create_response(db: Session, response: schemas.ResponseCreate) -> models.Response:
    """Create a new response in the database"""
    db_response = models.Response(
        query_id=UUID(response.query_id),
        response_text=response.response_text,
        source_chunks=response.source_chunks,
        token_usage=response.token_usage.dict() if response.token_usage else None
    )
    db.add(db_response)
    db.commit()
    db.refresh(db_response)
    return db_response


def get_response(db: Session, response_id: str) -> Optional[models.Response]:
    """Retrieve a response by ID"""
    response_uuid = UUID(response_id)
    return db.query(models.Response).filter(models.Response.response_id == response_uuid).first()


# User selection operations
def create_user_selection(db: Session, selection: schemas.UserSelectionCreate) -> models.UserSelection:
    """Create a new user selection in the database"""
    db_selection = models.UserSelection(
        session_id=UUID(selection.session_id),
        content=selection.content,
        source_location=selection.source_location,
        query_id=UUID(selection.query_id) if selection.query_id else None
    )
    db.add(db_selection)
    db.commit()
    db.refresh(db_selection)
    return db_selection