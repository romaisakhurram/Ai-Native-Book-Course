import asyncio
from typing import Optional, Dict, Any, AsyncGenerator
from models.chat_models import MessageContext
import time


class RAGService:
    """
    RAG (Retrieval-Augmented Generation) Service
    Handles the processing of queries with context, especially selected text
    """

    def __init__(self):
        # In a real implementation, this would connect to Qdrant or similar vector database
        # For this example, we'll simulate the process
        # We'll also maintain a simple in-memory session cache for demonstration
        self.session_cache: Dict[str, Any] = {}

    def _get_session_data(self, session_id: str) -> Dict[str, Any]:
        """Get or create session data for the given session ID"""
        if session_id not in self.session_cache:
            self.session_cache[session_id] = {
                "created_at": time.time(),
                "last_accessed": time.time(),
                "conversation_history": []
            }
        self.session_cache[session_id]["last_accessed"] = time.time()
        return self.session_cache[session_id]
    
    async def is_available(self) -> bool:
        """
        Check if the RAG service is available
        """
        # Simulate availability check
        # In a real implementation, this would check connectivity to required services
        return True
    
    async def process_query(
        self,
        query: str,
        session_id: str,
        context: Optional[MessageContext] = None
    ) -> str:
        """
        Process a query with optional context
        """
        # Get session data to maintain conversation history
        session_data = self._get_session_data(session_id)

        # Import the services needed for RAG functionality
        from services.retrieval_service import RetrievalService
        from services.chat_service import ChatService
        from models.schemas import QueryRequest, SourceChunk

        # Create an instance of the retrieval service to get relevant context
        retrieval_service = RetrievalService()

        # Determine query mode based on context
        query_mode = "SELECTED_TEXT_ONLY" if context and context.selectedText else "FULL_BOOK"
        selected_text = context.selectedText if context and context.selectedText else None

        # Retrieve relevant context from the vector database
        source_chunks = await retrieval_service.retrieve_context(
            query_text=query,
            query_mode=query_mode,
            selected_text=selected_text,
            limit=5  # Retrieve up to 5 relevant chunks
        )

        # Create a query request object - using the correct schema fields
        query_request = QueryRequest(
            query_text=query,
            query_mode=query_mode,
            selected_text=selected_text
        )

        # Create an instance of the chat service to generate the response
        chat_service = ChatService()

        try:
            # Generate the response using the retrieved context
            response_obj = await chat_service.generate_response(
                query_request=query_request,
                source_chunks=source_chunks
            )
        except Exception as e:
            # If there's an error generating the response, return a default error response
            from models.schemas import ResponseCreate, TokenUsage, SourceChunk
            response_obj = ResponseCreate(
                response_text="I'm sorry, I encountered an error while processing your request. Please try again.",
                source_chunks=[],
                token_usage=TokenUsage(input_tokens=0, output_tokens=0),
                query_id=f"query_{int(time.time())}_{abs(hash(query)) % 10000}"
            )

        # Add this interaction to the conversation history
        session_data = self._get_session_data(session_id)  # Get updated session data
        session_data["conversation_history"].append({
            "query": query,
            "context": context.dict() if context else None,
            "response": getattr(response_obj, 'response_text', response_obj if isinstance(response_obj, str) else "Error generating response"),
            "timestamp": time.time()
        })

        # Limit history to prevent it from growing indefinitely
        if len(session_data["conversation_history"]) > 50:  # Keep last 50 interactions
            session_data["conversation_history"] = session_data["conversation_history"][-50:]

        # Return the response text, with fallback if the response object doesn't have the expected structure
        return getattr(response_obj, 'response_text', response_obj if isinstance(response_obj, str) else "Error generating response")
    
    async def stream_response(
        self,
        query: str,
        session_id: str,
        context: Optional[MessageContext] = None
    ) -> AsyncGenerator[str, None]:
        """
        Stream response tokens as they are generated
        """
        # In a real implementation, this would stream tokens as they are generated by the LLM
        # For this example, we'll simulate streaming by yielding tokens one by one

        # Get the full response first (in a real streaming implementation, this would be different)
        response = await self.process_query(query, session_id, context)
        tokens = response.split()

        for i, token in enumerate(tokens):
            # Simulate processing delay for each token
            await asyncio.sleep(0.05)  # 50ms delay per token

            # Add space after token, except for the last one
            yield f"{token} " if i < len(tokens) - 1 else token
    
    async def retrieve_context(self, query: str, selected_text: Optional[str] = None) -> str:
        """
        Retrieve relevant context from the book content
        """
        # In a real implementation, this would query the vector database
        # For this example, we'll return a placeholder
        if selected_text:
            return f"Context from selected text: {selected_text[:200]}..."
        else:
            return "General context from the book..."