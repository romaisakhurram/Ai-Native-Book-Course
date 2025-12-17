"""
Pydantic schemas for request/response validation
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID, uuid4


# Chat Session Schemas
class ChatSessionBase(BaseModel):
    user_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class ChatSessionCreate(ChatSessionBase):
    pass


class ChatSession(ChatSessionBase):
    session_id: str
    created_at: datetime
    updated_at: datetime
    is_active: bool

    class Config:
        from_attributes = True


# Query Schemas
class QueryBase(BaseModel):
    query_text: str
    query_mode: str = Field(..., pattern="^(FULL_BOOK|SELECTED_TEXT_ONLY)$")
    selected_text: Optional[str] = None


class QueryCreate(QueryBase):
    session_id: str


class Query(QueryBase):
    query_id: str
    session_id: str
    timestamp: datetime
    source_reference: Optional[str] = None

    class Config:
        from_attributes = True


# Response Schemas
class SourceChunk(BaseModel):
    chunk_id: str
    content: str
    document_id: str
    metadata: Optional[Dict[str, Any]] = None


class TokenUsage(BaseModel):
    input_tokens: int
    output_tokens: int


class ResponseBase(BaseModel):
    response_text: str
    source_chunks: List[SourceChunk]
    token_usage: Optional[TokenUsage] = None


class ResponseCreate(ResponseBase):
    query_id: str


class Response(ResponseBase):
    response_id: str
    query_id: str
    timestamp: datetime

    class Config:
        from_attributes = True


# Book Content Chunk Schemas
class BookContentChunkBase(BaseModel):
    document_id: str
    content: str
    metadata: Optional[Dict[str, Any]] = None
    hash: Optional[str] = None


class BookContentChunkCreate(BookContentChunkBase):
    pass


class BookContentChunk(BookContentChunkBase):
    chunk_id: str
    embedding: Optional[List[float]] = None

    class Config:
        from_attributes = True


# User Selection Schemas
class UserSelectionBase(BaseModel):
    content: str
    source_location: str


class UserSelectionCreate(UserSelectionBase):
    session_id: str
    query_id: Optional[str] = None


class UserSelection(UserSelectionBase):
    selection_id: str
    session_id: str
    created_at: datetime
    query_id: Optional[str] = None

    class Config:
        from_attributes = True


# Request/Response Schemas for API endpoints
class SessionCreateRequest(BaseModel):
    user_id: str


class SessionCreateResponse(BaseModel):
    session_id: str
    created_at: datetime


class SessionResponse(BaseModel):
    session_id: str
    user_id: Optional[str]
    created_at: datetime
    updated_at: datetime
    is_active: bool


class QueryRequest(BaseModel):
    query_text: str
    query_mode: str = Field(..., pattern="^(FULL_BOOK|SELECTED_TEXT_ONLY)$")
    selected_text: Optional[str] = None


class QueryResponse(BaseModel):
    query_id: str
    session_id: str
    query_text: str
    response_text: str
    source_chunks: List[SourceChunk]
    timestamp: datetime


# Health check response
class HealthResponse(BaseModel):
    status: str