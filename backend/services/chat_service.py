"""
Chat service for generating responses based on retrieved context
"""
from typing import List, Dict, Any, Optional
import openai
import logging
import os
from models.schemas import QueryRequest, ResponseCreate, SourceChunk, TokenUsage
from .retrieval_service import RetrievalService

logger = logging.getLogger(__name__)

class ChatService:
    def __init__(self):
        self.retrieval_service = RetrievalService()

    async def generate_response(self, 
                               query_request: QueryRequest, 
                               source_chunks: List[SourceChunk]) -> ResponseCreate:
        """
        Generate a response to the user's query based on the retrieved context
        :param query_request: The user's query and related parameters
        :param source_chunks: Context chunks retrieved based on the query
        :return: The generated response
        """
        try:
            # Build the context from the source chunks
            context_text = self._build_context_text(source_chunks)

            # Log information about the context for debugging
            if not context_text or len(context_text.strip()) == 0:
                logger.warning(f"No context retrieved for query: {query_request.query_text}")
                logger.warning("This may result in a generic response from the LLM")
            else:
                logger.info(f"Using context of {len(context_text)} characters for query: {query_request.query_text[:50]}...")

            # Generate the response using the LLM
            response_text, token_usage = await self._call_llm(
                query_request.query_text,
                context_text,
                query_request.query_mode
            )
            
            # Create and return the response object
            response = ResponseCreate(
                response_text=response_text,
                source_chunks=source_chunks,
                token_usage=token_usage,
                query_id=f"query_{int(time.time())}_{hash(query_request.query_text) % 10000}"  # Generate a unique query ID
            )
            
            logger.info(f"Generated response for query: {query_request.query_text[:50]}...")
            return response
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            # Return a default error response
            return ResponseCreate(
                response_text="I'm sorry, I encountered an error while processing your request. Please try again.",
                source_chunks=[],
                token_usage=None
            )

    def _build_context_text(self, source_chunks: List[SourceChunk]) -> str:
        """
        Build the context text from the retrieved source chunks
        :param source_chunks: List of source chunks to build context from
        :return: Combined context text
        """
        if not source_chunks:
            return ""
        
        context_parts = []
        for chunk in source_chunks:
            context_parts.append(f"Document: {chunk.document_id}\nContent: {chunk.content}\n")
        
        return "\n".join(context_parts)

    async def _call_llm(self, query: str, context: str, query_mode: str) -> tuple[str, TokenUsage]:
        """
        Call the LLM to generate a response
        :param query: The user's query
        :param context: Context retrieved from the knowledge base
        :param query_mode: The query mode (FULL_BOOK or SELECTED_TEXT_ONLY)
        :return: The generated response text and token usage
        """
        try:
            # Configure OpenAI client with OpenRouter settings
            openai.base_url = "https://openrouter.ai/api/v1"
            openai.api_key = self._get_api_key()

            # Build the system message based on query mode
            if query_mode == "SELECTED_TEXT_ONLY":
                system_message = """You are a helpful assistant that answers questions based only on the provided text.
                Do not use any external knowledge. If the answer is not in the provided text,
                explicitly state that the answer is not available in the selected text."""
            else:
                system_message = """You are a helpful assistant that answers questions based on the provided book content.
                Only use information from the provided context to answer the user's question.
                Do not use any external knowledge or make up information."""

            # Construct the user message
            if context:
                user_message = f"""Based on the following context:\n\n{context}\n\nPlease answer the following question: {query}"""
            else:
                user_message = f"Please answer the following question: {query}. Note: No relevant context was found in the book content."

            # Call the LLM
            from config.settings import settings
            model_name = getattr(settings, 'openai_model', 'mistralai/mistral-7b-instruct:free')
            response = openai.chat.completions.create(
                model=model_name,  # Use model from settings
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.7,  # Balance between creativity and consistency
                max_tokens=500  # Limit response length
            )

            # Extract the response text
            response_text = response.choices[0].message.content

            # Extract token usage
            token_usage = TokenUsage(
                input_tokens=response.usage.prompt_tokens if hasattr(response, 'usage') and response.usage else 0,
                output_tokens=response.usage.completion_tokens if hasattr(response, 'usage') and response.usage else 0
            )

            return response_text, token_usage
        except openai.AuthenticationError as e:
            logger.error(f"Authentication error with OpenRouter API: {e}")
            # Return a default response when API key is invalid
            error_text = "I'm sorry, there is an issue with the AI service configuration. Please contact the administrator."
            error_tokens = TokenUsage(input_tokens=0, output_tokens=0)
            return error_text, error_tokens
        except openai.RateLimitError as e:
            logger.error(f"Rate limit error with OpenRouter API: {e}")
            # Return a default response when rate limit is exceeded
            error_text = "I'm sorry, the AI service is temporarily overloaded. Please try again in a moment."
            error_tokens = TokenUsage(input_tokens=0, output_tokens=0)
            return error_text, error_tokens
        except openai.APIError as e:
            logger.error(f"API error with OpenRouter API: {e}")
            # Handle other API errors
            error_text = "I'm sorry, I'm currently experiencing issues with the AI service. Please try again later."
            error_tokens = TokenUsage(input_tokens=0, output_tokens=0)
            return error_text, error_tokens
        except Exception as e:
            logger.error(f"Error calling LLM: {e}")
            # Return a default error response
            error_text = "I'm sorry, I'm currently unable to generate a response. Please try again later."
            error_tokens = TokenUsage(input_tokens=0, output_tokens=0)
            return error_text, error_tokens

    def _get_api_key(self) -> str:
        """
        Get the OpenRouter API key from settings
        """
        # Access the API key from the settings module
        from config.settings import settings
        # Try getting the key from settings first, then from environment variables
        api_key = getattr(settings, 'openrouter_api_key', None) or getattr(settings, 'openai_api_key', None) or \
                  os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENAI_API_KEY")
        if not api_key:
            # If no API key is available, return a mock key for testing
            # In a real application, you would want to handle this differently
            logger.warning("No API key found in settings or environment, using mock API key for testing")
            return "sk-test-key-for-testing-only-do-not-use-in-production"
        return api_key

    async def validate_response_quality(self, response: str, query: str) -> bool:
        """
        Validate if the response is of sufficient quality
        :param response: The generated response text
        :param query: The original query
        :return: True if the response is of good quality, False otherwise
        """
        # Basic validation checks
        if not response or not response.strip():
            return False
        
        # Check if response contains common failure indicators
        lower_response = response.lower()
        if "i don't know" in lower_response or "i don't have" in lower_response:
            # This might be a valid response if no context was available, so we'll allow it
            pass
        
        # Additional quality checks could be implemented here
        # For example, checking if the response actually addresses the query
        
        return True