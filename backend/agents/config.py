"""
Configuration settings for the AI-Native Book Course backend
Extends the main settings with agent-specific configurations
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class AgentSettings(BaseSettings):
    """
    Settings specifically for the AI agent
    """
    # Model configuration
    agent_model: str = os.getenv("AGENT_MODEL", "mistralai/devstral-2512:free")
    
    # API configuration
    openrouter_api_key: str = os.getenv("OPENROUTER_API_KEY", "")
    openrouter_base_url: str = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
    
    # Agent behavior settings
    agent_temperature: float = float(os.getenv("AGENT_TEMPERATURE", "0.7"))
    agent_max_tokens: int = int(os.getenv("AGENT_MAX_TOKENS", "500"))
    agent_timeout: int = int(os.getenv("AGENT_TIMEOUT", "30"))
    
    # System message for the agent
    agent_system_message: Optional[str] = os.getenv("AGENT_SYSTEM_MESSAGE")
    
    # Default system message if not provided
    @property
    def default_system_message(self) -> str:
        return (
            "You are a helpful assistant for the AI-Native Book Course. "
            "Answer questions based on the provided context from the book. "
            "If the answer is not available in the context, say so explicitly. "
            "Be concise and accurate in your responses."
        )

# Create an instance of agent settings
agent_settings = AgentSettings()