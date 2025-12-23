"""
API routes for query processing
"""
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from datetime import datetime
from uuid import UUID
from ...models.database import get_db
from ...models import schemas
from ...utils import db_operations
from ...services.chat_service import ChatService
from ...services.retrieval_service import RetrievalService
from sqlalchemy.orm import Session
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/sessions/{session_id}/queries", response_model=schemas.QueryResponse)
async def submit_query(
    session_id: str,
    query_request: schemas.QueryRequest,
    db: Session = Depends(get_db)
):
    """
    Submit a question to the chatbot within a session
    """
    try:
        # Validate that the session exists
        session_uuid = UUID(session_id)
        db_session = db_operations.get_session(db, session_id)
        if not db_session:
            raise HTTPException(status_code=404, detail="Session not found")

        # Validate the query request
        retrieval_service = RetrievalService()
        is_valid = await retrieval_service.validate_query_context(
            query_request.query_text,
            query_request.query_mode,
            query_request.selected_text
        )
        if not is_valid:
            raise HTTPException(status_code=400, detail="Invalid query request")

        # Create a query record in the database
        query_create = schemas.QueryCreate(
            session_id=session_id,
            query_text=query_request.query_text,
            query_mode=query_request.query_mode,
            selected_text=query_request.selected_text
        )
        db_query = db_operations.create_query(db, query_create)

        # Retrieve relevant context based on the query
        retrieval_service = RetrievalService()
        source_chunks = await retrieval_service.retrieve_context(
            query_request.query_text,
            query_request.query_mode,
            query_request.selected_text
        )

        # Generate a response using the chat service
        chat_service = ChatService()
        response_create = await chat_service.generate_response(query_request, source_chunks)

        # Update the response_create to link to the query we just made
        response_create.query_id = str(db_query.query_id)

        # Create the response record in the database
        db_response = db_operations.create_response(db, response_create)

        # Return the complete response
        return schemas.QueryResponse(
            query_id=str(db_query.query_id),
            session_id=session_id,
            query_text=db_query.query_text,
            response_text=db_response.response_text,
            source_chunks=source_chunks,
            timestamp=db_response.timestamp
        )
    except ValueError:
        # This happens if session_id or other IDs are not valid UUIDs
        raise HTTPException(status_code=400, detail="Invalid ID format")
    except HTTPException:
        # Re-raise HTTP exceptions to maintain the same behavior
        raise
    except Exception as e:
        logger.error(f"Error processing query for session {session_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error during query processing")

@router.get("/sessions/{session_id}/queries/{query_id}", response_model=schemas.QueryResponse)
def get_query_response(
    session_id: str,
    query_id: str,
    db: Session = Depends(get_db)
):
    """
    Retrieve a previously asked question and its answer
    """
    try:
        # Validate that the IDs are valid UUIDs
        session_uuid = UUID(session_id)
        query_uuid = UUID(query_id)

        # Check if the session exists
        db_session = db_operations.get_session(db, session_id)
        if not db_session:
            raise HTTPException(status_code=404, detail="Session not found")

        # Get the query from the database
        db_query = db_operations.get_query(db, query_id)
        if not db_query:
            raise HTTPException(status_code=404, detail="Query not found")

        # Verify that the query belongs to the specified session
        if str(db_query.session_id) != session_id:
            raise HTTPException(status_code=404, detail="Query does not belong to the specified session")

        # Get the response for this query
        db_response = db_query.response
        if not db_response:
            raise HTTPException(status_code=404, detail="Response not found for this query")

        # For source chunks, we need to extract them from the response's source_chunks field
        # These were stored as JSON, so we need to convert them back to SourceChunk objects
        source_chunks = []
        if db_response.source_chunks:
            for chunk_data in db_response.source_chunks:
                source_chunk = schemas.SourceChunk(
                    chunk_id=chunk_data.get('chunk_id', ''),
                    content=chunk_data.get('content', ''),
                    document_id=chunk_data.get('document_id', ''),
                    metadata=chunk_data.get('metadata', {})
                )
                source_chunks.append(source_chunk)

        # Return the query and its response
        return schemas.QueryResponse(
            query_id=str(db_query.query_id),
            session_id=session_id,
            query_text=db_query.query_text,
            response_text=db_response.response_text,
            source_chunks=source_chunks,
            timestamp=db_response.timestamp
        )
    except ValueError:
        # This happens if session_id or query_id are not valid UUIDs
        raise HTTPException(status_code=400, detail="Invalid ID format")
    except HTTPException:
        # Re-raise HTTP exceptions to maintain the same behavior
        raise
    except Exception as e:
        logger.error(f"Error retrieving query {query_id} for session {session_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error during query retrieval")