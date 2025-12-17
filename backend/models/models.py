"""
SQLAlchemy ORM models for the RAG Chatbot
"""
from sqlalchemy import Column, String, DateTime, Boolean, Text, Integer, UUID, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import declarative_base, relationship
from .database import Base
from datetime import datetime
import uuid

class ChatSession(Base):
    __tablename__ = "chat_sessions"

    session_id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(String, nullable=True)  # Optional for anonymous sessions
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    session_metadata = Column(JSON, nullable=True)
    is_active = Column(Boolean, default=True)

    # Relationship to queries
    queries = relationship("Query", back_populates="session")


class Query(Base):
    __tablename__ = "queries"

    query_id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(PG_UUID(as_uuid=True), ForeignKey("chat_sessions.session_id"))
    query_text = Column(Text, nullable=False)
    query_mode = Column(String(50), nullable=False)  # 'FULL_BOOK' or 'SELECTED_TEXT_ONLY'
    selected_text = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    source_reference = Column(String, nullable=True)  # Reference to page/chapter

    # Relationship to session
    session = relationship("ChatSession", back_populates="queries")

    # Relationship to response
    response = relationship("Response", back_populates="query", uselist=False)


class Response(Base):
    __tablename__ = "responses"

    response_id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    query_id = Column(PG_UUID(as_uuid=True), ForeignKey("queries.query_id"))
    response_text = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    source_chunks = Column(JSON)  # Store as JSON array
    token_usage = Column(JSON)  # Store as JSON object {input_tokens: int, output_tokens: int}

    # Relationship to query
    query = relationship("Query", back_populates="response")


class BookContentChunk(Base):
    __tablename__ = "Ai-book"

    chunk_id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id = Column(String, nullable=False)  # Identifier for the source document
    content = Column(Text, nullable=False)  # The actual content chunk
    chunk_metadata = Column(JSON)  # Source location, headings, etc.
    embedding = Column(String, nullable=True)  # Serialized embedding vector
    hash = Column(String, nullable=True)  # For change detection

    def __repr__(self):
        return f"<BookContentChunk(document_id='{self.document_id}', chunk_id='{self.chunk_id}')>"


class UserSelection(Base):
    __tablename__ = "user_selections"

    selection_id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(PG_UUID(as_uuid=True), ForeignKey("chat_sessions.session_id"))
    content = Column(Text, nullable=False)  # The selected text
    source_location = Column(String, nullable=False)  # Where in the book this text appears
    created_at = Column(DateTime, default=datetime.utcnow)
    query_id = Column(PG_UUID(as_uuid=True), ForeignKey("queries.query_id"), nullable=True)

    # Relationships
    session = relationship("ChatSession")
    query = relationship("Query")