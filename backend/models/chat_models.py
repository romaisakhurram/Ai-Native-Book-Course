from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class MessageContext(BaseModel):
    selectedText: Optional[str] = None
    sourcePage: str
    selectionMetadata: Optional[dict] = None


class ChatRequest(BaseModel):
    message: str
    sessionId: str
    context: Optional[MessageContext] = None


class ChatResponse(BaseModel):
    responseId: str
    content: str
    timestamp: datetime
    status: str  # 'success' or 'error'
    streamComplete: bool = False


class ErrorResponse(BaseModel):
    error: str
    code: str
    details: Optional[dict] = None