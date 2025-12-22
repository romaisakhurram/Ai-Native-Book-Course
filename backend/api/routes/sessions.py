"""
API routes for session management
"""
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from datetime import datetime
from uuid import UUID
from models.database import get_db
from models import schemas
from utils import db_operations
from sqlalchemy.orm import Session
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/sessions", response_model=schemas.SessionCreateResponse)
def create_session(session_request: schemas.SessionCreateRequest, db: Session = Depends(get_db)):
    """
    Create a new chat session
    """
    try:
        # Create a ChatSessionCreate object from the request
        session_create = schemas.ChatSessionCreate(
            user_id=session_request.user_id,
            metadata=None  # No initial metadata in this simple case
        )

        # Use the db_operations utility to create the session in the database
        db_session = db_operations.create_session(db, session_create)

        return schemas.SessionCreateResponse(
            session_id=str(db_session.session_id),
            created_at=db_session.created_at
        )
    except Exception as e:
        logger.error(f"Error creating session: {e}")
        raise HTTPException(status_code=500, detail="Internal server error during session creation")

@router.get("/sessions/{session_id}", response_model=schemas.SessionResponse)
def get_session(session_id: str, db: Session = Depends(get_db)):
    """
    Get details about a specific chat session
    """
    try:
        # Convert session_id to UUID to ensure proper format
        session_uuid = UUID(session_id)

        # Use the db_operations utility to retrieve the session from the database
        db_session = db_operations.get_session(db, session_id)

        if not db_session:
            raise HTTPException(status_code=404, detail="Session not found")

        return schemas.SessionResponse(
            session_id=str(db_session.session_id),
            user_id=db_session.user_id,
            created_at=db_session.created_at,
            updated_at=db_session.updated_at,
            is_active=db_session.is_active
        )
    except ValueError:
        # This happens if session_id is not a valid UUID
        raise HTTPException(status_code=400, detail="Invalid session ID format")
    except HTTPException:
        # Re-raise HTTP exceptions (like 404) to maintain the same behavior
        raise
    except Exception as e:
        logger.error(f"Error retrieving session {session_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error during session retrieval")

@router.get("/sessions/{session_id}/history", response_model=List[schemas.QueryResponse])
def get_session_history(session_id: str, db: Session = Depends(get_db)):
    """
    Get the history of queries and responses for a specific session
    """
    try:
        # Convert session_id to UUID
        session_uuid = UUID(session_id)

        # Verify that the session exists
        db_session = db_operations.get_session(db, session_id)
        if not db_session:
            raise HTTPException(status_code=404, detail="Session not found")

        # Get all queries associated with the session
        # We need to query the database directly since we don't have a helper function for this
        from api.models import models
        queries = db.query(models.Query).filter(models.Query.session_id == session_uuid).all()

        # For each query, get its response and build the history
        history = []
        for query in queries:
            # Get the response for this query
            response = query.response

            if response:
                # Extract source chunks from the response (stored as JSON)
                source_chunks = []
                if response.source_chunks:
                    for chunk_data in response.source_chunks:
                        source_chunk = schemas.SourceChunk(
                            chunk_id=chunk_data.get('chunk_id', ''),
                            content=chunk_data.get('content', ''),
                            document_id=chunk_data.get('document_id', ''),
                            metadata=chunk_data.get('metadata', {})
                        )
                        source_chunks.append(source_chunk)

                # Build the QueryResponse object for this query-response pair
                query_response = schemas.QueryResponse(
                    query_id=str(query.query_id),
                    session_id=session_id,
                    query_text=query.query_text,
                    response_text=response.response_text,
                    source_chunks=source_chunks,
                    timestamp=response.timestamp
                )
                history.append(query_response)

        # Sort history by timestamp to ensure chronological order
        history.sort(key=lambda x: x.timestamp)

        return history
    except ValueError:
        # This happens if session_id is not a valid UUID
        raise HTTPException(status_code=400, detail="Invalid session ID format")
    except HTTPException:
        # Re-raise HTTP exceptions (like 404) to maintain the same behavior
        raise
    except Exception as e:
        logger.error(f"Error retrieving session history {session_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error during session history retrieval")

@router.delete("/sessions/{session_id}")
def delete_session(session_id: str, db: Session = Depends(get_db)):
    """
    Delete a chat session and all its associated data (queries, responses)
    """
    try:
        # Convert session_id to UUID
        session_uuid = UUID(session_id)

        # Verify that the session exists
        db_session = db_operations.get_session(db, session_id)
        if not db_session:
            raise HTTPException(status_code=404, detail="Session not found")

        # Mark the session as inactive (soft delete approach)
        db_session.is_active = False
        db.commit()

        return {"message": f"Session {session_id} marked as inactive"}
    except ValueError:
        # This happens if session_id is not a valid UUID
        raise HTTPException(status_code=400, detail="Invalid session ID format")
    except HTTPException:
        # Re-raise HTTP exceptions (like 404) to maintain the same behavior
        raise
    except Exception as e:
        logger.error(f"Error deleting session {session_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error during session deletion")

@router.put("/sessions/{session_id}/deactivate")
def deactivate_session(session_id: str, db: Session = Depends(get_db)):
    """
    Deactivate a chat session (set is_active to False)
    """
    try:
        # Convert session_id to UUID
        session_uuid = UUID(session_id)

        # Get the session from database
        db_session = db_operations.get_session(db, session_id)
        if not db_session:
            raise HTTPException(status_code=404, detail="Session not found")

        # Mark the session as inactive
        db_session.is_active = False
        db.commit()

        return {"message": f"Session {session_id} deactivated successfully"}
    except ValueError:
        # This happens if session_id is not a valid UUID
        raise HTTPException(status_code=400, detail="Invalid session ID format")
    except HTTPException:
        # Re-raise HTTP exceptions (like 404) to maintain the same behavior
        raise
    except Exception as e:
        logger.error(f"Error deactivating session {session_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error during session deactivation")