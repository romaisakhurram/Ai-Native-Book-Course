from pydantic_settings import BaseSettings
from typing import Optional
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    # API Configuration
    openrouter_api_key: str = os.getenv("OPENROUTER_API_KEY", "")
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_model: str = os.getenv("OPENAI_MODEL", "qwen/qwen3-embedding-8b")
    openrouter_base_url: str = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1/chat/completions")
    qdrant_url: str = os.getenv("QDRANT_URL", "")
    qdrant_api_key: str = os.getenv("QDRANT_API_KEY", "")
    qdrant_base_url: str = os.getenv("QDRANT_BASE_URL", "https://localhost:6333")
    neon_database_url: str = os.getenv("NEON_DATABASE_URL", "sqlite:///./rag_chatbot.db")

    # Application settings
    app_name: str = "RAG Chatbot API for Markdown Book"
    app_version: str = "1.0.0"
    debug: bool = False
    log_level: str = os.getenv("LOG_LEVEL", "info")

    # Qdrant settings
    qdrant_collection_name: str = "Ai-book"

    # Database settings
    db_echo: bool = False  # Set to True for SQL query logging

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # Ignore extra environment variables

settings = Settings()