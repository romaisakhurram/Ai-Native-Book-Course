"""
Agent configuration for the AI-Native Book Course
This file contains the agent implementation using the specified model and API settings
"""
import os
import openai
from typing import Dict, Any, Optional
from pydantic import BaseModel
from config.settings import settings

class AgentConfig(BaseModel):
    """
    Configuration for the AI agent
    """
    model: str = "mistralai/devstral-2512:free"
    base_url: str = "https://openrouter.ai/api/v1"
    temperature: float = 0.7
    max_tokens: int = 500
    timeout: int = 30

class Agent:
    """
    AI Agent for processing queries and generating responses
    """
    
    def __init__(self, config: Optional[AgentConfig] = None):
        """
        Initialize the agent with configuration
        """
        self.config = config or AgentConfig()
        
        # Set up OpenAI client with OpenRouter settings
        openai.base_url = self.config.base_url
        openai.api_key = self._get_api_key()
        
        # Additional configuration from settings
        self.system_message = settings.agent_system_message or self._default_system_message()
    
    def _get_api_key(self) -> str:
        """
        Get the API key from environment or settings
        """
        api_key = os.getenv("OPENROUTER_API_KEY") or settings.openrouter_api_key
        if not api_key:
            raise ValueError("OpenRouter API key not found in environment or settings")
        return api_key
    
    def _default_system_message(self) -> str:
        """
        Default system message for the agent
        """
        return (
            "You are a helpful assistant for the AI-Native Book Course. "
            "Answer questions based on the provided context from the book. "
            "If the answer is not available in the context, say so explicitly. "
            "Be concise and accurate in your responses."
        )
    
    async def process_query(self, query: str, context: Optional[str] = None) -> Dict[str, Any]:
        """
        Process a query with optional context and return a response
        """
        try:
            # Build the user message with context if provided
            if context:
                user_message = f"Context: {context}\n\nQuestion: {query}"
            else:
                user_message = f"Question: {query}"
            
            # Call the LLM
            response = openai.chat.completions.create(
                model=self.config.model,
                messages=[
                    {"role": "system", "content": self.system_message},
                    {"role": "user", "content": user_message}
                ],
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens
            )
            
            # Extract response and token usage
            response_text = response.choices[0].message.content
            token_usage = {
                "input_tokens": response.usage.prompt_tokens if response.usage else 0,
                "output_tokens": response.usage.completion_tokens if response.usage else 0
            }
            
            return {
                "response": response_text,
                "token_usage": token_usage,
                "model": self.config.model,
                "success": True
            }
        except Exception as e:
            # Log the error
            print(f"Error processing query: {e}")
            
            # Return an error response
            return {
                "response": "I'm sorry, I encountered an error while processing your query. Please try again.",
                "token_usage": {"input_tokens": 0, "output_tokens": 0},
                "model": self.config.model,
                "success": False,
                "error": str(e)
            }
    
    def update_system_message(self, new_system_message: str):
        """
        Update the system message for the agent
        """
        self.system_message = new_system_message

# Create a default agent instance
default_agent = Agent()

async def query_agent(query: str, context: Optional[str] = None):
    """
    Convenience function to query the default agent
    """
    return await default_agent.process_query(query, context)