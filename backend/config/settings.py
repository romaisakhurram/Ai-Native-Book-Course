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
    openai_model: str = os.getenv("OPENAI_MODEL", " mistralai/devstral-2512:free")
    openrouter_base_url: str = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
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

    # Agent settings
    agent_model: str = os.getenv("AGENT_MODEL", "mistralai/devstral-2512:free")
    agent_temperature: float = float(os.getenv("AGENT_TEMPERATURE", "0.7"))
    agent_max_tokens: int = int(os.getenv("AGENT_MAX_TOKENS", "500"))
    agent_system_message: Optional[str] = os.getenv("AGENT_SYSTEM_MESSAGE")

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # Ignore extra environment variables

settings = Settings()