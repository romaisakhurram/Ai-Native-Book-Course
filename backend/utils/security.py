"""
Security utilities and middleware for the RAG Chatbot API
"""
from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from jwt import PyJWTError
from typing import Optional
import os
import logging

logger = logging.getLogger(__name__)

# Initialize security schemes
security = HTTPBearer()

def verify_token(token: str) -> Optional[dict]:
    """
    Verify the provided JWT token
    In a real implementation, you would check the token against your auth provider
    """
    try:
        # In a production environment, you'd verify against a secret key
        # payload = jwt.decode(token, os.getenv("JWT_SECRET"), algorithms=["HS256"])
        # For now, we'll just return a mock payload for demonstration
        if token in ["mock-valid-token", os.getenv("API_KEY", "test-key")]:
            return {"user_id": "mock-user", "role": "user"}
        else:
            return None
    except PyJWTError:
        logger.error("Token verification failed")
        return None

def get_current_user(credentials: HTTPAuthorizationCredentials = security):
    """
    Get the current user from the provided credentials
    """
    token = credentials.credentials
    user = verify_token(token)
    if not user:
        logger.warning("Authentication failed for token")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

# Additional security utilities
def sanitize_input(input_text: str) -> str:
    """
    Sanitize user input to prevent injection attacks
    """
    # Remove potentially dangerous characters
    sanitized = input_text.replace('<script', '&lt;script').replace('javascript:', 'javascript&#58;')
    return sanitized

def validate_content_length(text: str, max_length: int = 5000) -> bool:
    """
    Validate that content is not excessively long
    """
    return len(text) <= max_length

def validate_session_id(session_id: str) -> bool:
    """
    Validate session ID format to prevent session fixation attacks
    """
    import uuid
    try:
        uuid.UUID(session_id)
        return True
    except ValueError:
        return False