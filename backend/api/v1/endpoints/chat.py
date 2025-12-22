from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import Dict, Any
import asyncio
import json
from datetime import datetime

from ...models.chat_models import ChatRequest, ChatResponse, ErrorResponse
from ...core.rag_service import RAGService

router = APIRouter()
rag_service = RAGService()

# In-memory storage for queued messages (in production, use a proper queue like Celery)
queued_messages: Dict[str, Any] = {}

@router.post("/chat/start", response_model=dict)
async def start_chat():
    """
    Start a new chat session
    """
    try:
        session_id = f"sess_{int(datetime.now().timestamp())}_{hash(str(datetime.now())) % 10000}"
        return {
            "sessionId": session_id,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/chat/send", response_model=ChatResponse)
async def send_message(chat_request: ChatRequest):
    """
    Send a message and get a response
    """
    try:
        # Use RAG service to generate response with context
        response_content = await rag_service.process_query(
            chat_request.message,
            chat_request.sessionId,
            chat_request.context
        )
        
        response = ChatResponse(
            responseId=f"resp_{int(datetime.now().timestamp())}",
            content=response_content,
            timestamp=datetime.now(),
            status="success"
        )
        
        return response
    except Exception as e:
        error_resp = ErrorResponse(
            error=str(e),
            code="PROCESSING_ERROR",
            details={"sessionId": chat_request.sessionId}
        )
        raise HTTPException(status_code=500, detail=error_resp.json())


@router.post("/chat/stream")
async def stream_message(chat_request: ChatRequest):
    """
    Send a message and stream the response using Server-Sent Events
    Implements message queuing for service unavailability
    """
    from fastapi.responses import StreamingResponse
    
    async def event_generator():
        try:
            # Check if the AI service is available
            service_available = rag_service.is_available()
            
            if not service_available:
                # Add to queue and notify that message is queued
                queued_id = f"queue_{int(datetime.now().timestamp())}"
                queued_messages[queued_id] = {
                    "request": chat_request.dict(),
                    "timestamp": datetime.now().isoformat(),
                    "status": "queued"
                }
                
                yield f"data: {json.dumps({'content': '', 'done': True, 'status': 'queued'})}\n\n"
                return

            # Stream the response
            async for token in rag_service.stream_response(
                chat_request.message,
                chat_request.sessionId,
                chat_request.context
            ):
                yield f"data: {json.dumps({'content': token, 'done': False, 'status': 'success'})}\n\n"
                
            yield f"data: {json.dumps({'content': '', 'done': True, 'status': 'success'})}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'content': '', 'done': True, 'status': 'error', 'error': str(e)})}\n\n"
    
    return StreamingResponse(event_generator(), media_type="text/event-stream")