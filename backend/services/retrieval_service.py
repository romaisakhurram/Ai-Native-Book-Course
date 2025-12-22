"""
Retrieval service for performing semantic search over book content
"""
from typing import List, Dict, Any, Optional
import logging
from models.schemas import QueryRequest, SourceChunk
from .embedding_service import EmbeddingService
from utils.caching import cache_result

logger = logging.getLogger(__name__)

class RetrievalService:
    def __init__(self):
        self.embedding_service = EmbeddingService()

    @cache_result(expire=1800)  # Cache results for 30 minutes
    async def retrieve_context(self,
                              query_text: str,
                              query_mode: str,
                              selected_text: Optional[str] = None,
                              limit: int = 5) -> List[SourceChunk]:
        """
        Retrieve relevant content based on the query and mode
        :param query_text: The user's question
        :param query_mode: Either 'FULL_BOOK' or 'SELECTED_TEXT_ONLY'
        :param selected_text: Text selected by user (for SELECTED_TEXT_ONLY mode)
        :param limit: Maximum number of chunks to retrieve
        :return: List of relevant source chunks
        """
        try:
            if query_mode == "SELECTED_TEXT_ONLY" and selected_text:
                # In selected-text mode, only use the provided selected text
                return self._create_source_chunks_from_selected_text(selected_text, query_text)
            elif query_mode == "FULL_BOOK":
                # In full-book mode, perform semantic search across all content
                return await self._retrieve_from_full_book(query_text, limit)
            else:
                # Default to full-book search if mode is invalid
                logger.warning(f"Invalid query mode: {query_mode}, defaulting to FULL_BOOK")
                return await self._retrieve_from_full_book(query_text, limit)
        except Exception as e:
            logger.error(f"Error in retrieve_context: {e}")
            # Return empty list on error, but in a real system you might want to raise an exception
            return []

    async def _retrieve_from_full_book(self, query_text: str, limit: int) -> List[SourceChunk]:
        """
        Perform semantic search across the full book content
        :param query_text: The query text to search for
        :param limit: Maximum number of results to return
        :return: List of source chunks
        """
        # Use the embedding service to search for similar content
        search_results = await self.embedding_service.search_similar(query_text, limit)

        # Convert search results to SourceChunk objects
        source_chunks = []
        for result in search_results:
            source_chunk = SourceChunk(
                chunk_id=result["chunk_id"],
                content=result["content"],
                document_id=result["document_id"],
                metadata=result.get("metadata", {})
            )
            source_chunks.append(source_chunk)

        logger.info(f"Retrieved {len(source_chunks)} chunks for query: {query_text[:50]}...")
        return source_chunks

    def _create_source_chunks_from_selected_text(self, selected_text: str, query_text: str) -> List[SourceChunk]:
        """
        Create source chunks using only the user's selected text
        :param selected_text: The text that the user selected/highlighted
        :param query_text: The user's original query
        :return: List of source chunks
        """
        # Create a single source chunk using the selected text
        source_chunk = SourceChunk(
            chunk_id="selected-text",  # Use a constant ID for selected text
            content=selected_text,
            document_id="selected-text-source",  # Use a placeholder document ID
            metadata={
                "source": "user-selected",
                "query": query_text
            }
        )

        logger.info(f"Created source chunk from selected text for query: {query_text[:50]}...")
        return [source_chunk]

    async def validate_query_context(self,
                                   query_text: str,
                                   query_mode: str,
                                   selected_text: Optional[str] = None) -> bool:
        """
        Validate that we have sufficient context for the query
        :param query_text: The user's question
        :param query_mode: Either 'FULL_BOOK' or 'SELECTED_TEXT_ONLY'
        :param selected_text: Text selected by user (for SELECTED_TEXT_ONLY mode)
        :return: True if context is sufficient, False otherwise
        """
        try:
            # Check if query_mode is valid
            if query_mode not in ["FULL_BOOK", "SELECTED_TEXT_ONLY"]:
                logger.error(f"Invalid query mode: {query_mode}")
                return False

            # Check if required fields are present
            if not query_text or not query_text.strip():
                logger.error("Query text is empty")
                return False

            if query_mode == "SELECTED_TEXT_ONLY" and (not selected_text or not selected_text.strip()):
                logger.error("Selected text is required for SELECTED_TEXT_ONLY mode")
                return False

            # For selected text mode, just ensure selected text is provided
            if query_mode == "SELECTED_TEXT_ONLY":
                return True

            # For full book mode, we can check if there's content in the database
            # For now, we'll assume the content exists; in a real implementation
            # you'd check the actual vector database
            return True
        except Exception as e:
            logger.error(f"Error validating query context: {e}")
            return False