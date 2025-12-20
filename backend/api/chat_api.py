from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import logging
from services.book_content_service import BookContentService
from services.qdrant_service import QdrantService

router = APIRouter()
logger = logging.getLogger(__name__)

# Initialize services
book_service = BookContentService()
qdrant_service = QdrantService()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    sources: List[Dict[str, Any]] = []

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Main chat endpoint that processes user queries and returns AI-generated responses
    """
    try:
        # Search for relevant content in the book
        search_results = qdrant_service.search(request.message, limit=5)
        
        # Prepare context from search results
        context = "\n".join([result.payload.get("content", "") for result in search_results])
        
        # Generate response using the LLM with context
        response = book_service.generate_response(request.message, context)
        
        # Extract source documents for citations
        sources = [
            {
                "title": result.payload.get("title", ""),
                "url": result.payload.get("url", ""),
                "content": result.payload.get("content", "")[:200] + "..."
            }
            for result in search_results
        ]
        
        return ChatResponse(response=response, sources=sources)
    
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/health")
async def health_check():
    """
    Health check endpoint to verify the chat API is operational
    """
    return {"status": "healthy", "service": "chat-api"}