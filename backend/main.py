from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .config.settings import settings
from .models.database import engine, Base
from .middleware.request_logging import RequestLoggingMiddleware
from .middleware.rate_limit import RateLimitMiddleware
from .utils.logging_config import setup_logging, get_logger

# Configure logging
setup_logging()
logger = get_logger(__name__)

# Create FastAPI app instance
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
)

# Add middleware (order matters: last added is first executed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(RateLimitMiddleware, requests_limit=100, window_seconds=3600)  # 100 requests per hour
app.add_middleware(RequestLoggingMiddleware)

# Import API routes here to avoid circular imports
from .api.routes import sessions, queries
from .api.v1.endpoints.chat import router as chat_router

app.include_router(sessions.router, prefix="/api/v1", tags=["sessions"])
app.include_router(queries.router, prefix="/api/v1", tags=["queries"])
app.include_router(chat_router, prefix="/api/v1", tags=["chat"])

@app.on_event("startup")
async def startup_event():
    """
    Initialize database tables on startup
    """
    logger.info("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully")

@app.get("/")
def read_root():
    """
    Root endpoint to check if the API is running
    """
    return {"message": "RAG Chatbot API for Markdown Book", "version": settings.app_version}

@app.get("/health")
def health_check():
    """
    Health check endpoint
    """
    return {"status": "healthy"}

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return {"error": "Endpoint not found"}

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return {"error": "Internal server error"}