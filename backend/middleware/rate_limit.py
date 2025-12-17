"""
Rate limiting and error handling middleware for the RAG Chatbot API
"""
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp
from collections import defaultdict
import time
import logging
from typing import Dict

logger = logging.getLogger(__name__)

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, requests_limit: int = 100, window_seconds: int = 3600):
        super().__init__(app)
        self.requests_limit = requests_limit
        self.window_seconds = window_seconds
        self.requests: Dict[str, list] = defaultdict(list)

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        current_time = time.time()
        
        # Clean old requests outside the window
        self.requests[client_ip] = [
            req_time for req_time in self.requests[client_ip] 
            if current_time - req_time < self.window_seconds
        ]
        
        # Check if rate limit exceeded
        if len(self.requests[client_ip]) >= self.requests_limit:
            logger.warning(f"Rate limit exceeded for IP: {client_ip}")
            return Response(
                content="Rate limit exceeded. Please try again later.",
                status_code=429
            )
        
        # Add current request
        self.requests[client_ip].append(current_time)
        
        response: Response = await call_next(request)
        return response