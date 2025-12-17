"""
Request processing middleware for the RAG Chatbot API
"""
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp
import time
import logging

logger = logging.getLogger(__name__)

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # Log the incoming request
        logger.info(f"Incoming request: {request.method} {request.url}")
        
        try:
            response: Response = await call_next(request)
        except Exception as e:
            # Log any exceptions that occur
            logger.error(f"Request error: {request.method} {request.url} - {str(e)}")
            raise
        finally:
            # Calculate and log the response time
            process_time = time.time() - start_time
            response.headers["X-Process-Time"] = str(process_time)
            
            logger.info(f"Request completed: {request.method} {request.url} - {response.status_code} - {process_time:.4f}s")
        
        return response