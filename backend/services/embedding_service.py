"""
Embedding service for generating and managing vector embeddings
"""
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import Distance, VectorParams
from typing import List, Dict, Any, Optional
import openai
import asyncio
import logging
from ..config.settings import settings
from ..models.schemas import BookContentChunkCreate

logger = logging.getLogger(__name__)

class EmbeddingService:
    def __init__(self):
        # Initialize Qdrant client
        self.client = QdrantClient(
            url=settings.qdrant_url,
            api_key=settings.qdrant_api_key,
            prefer_grpc=False  # Using HTTP API
        )
        self.collection_name = settings.qdrant_collection_name
        self._ensure_collection_exists()

    def _ensure_collection_exists(self):
        """
        Check if the collection exists, if not create it
        """
        try:
            # Determine the embedding size based on the model being used
            # Qwen3-embedding-8b produces 4096-dimensional vectors
            # text-embedding-ada-002 produces 1536-dimensional vectors
            model_name = getattr(settings, 'openai_model', 'text-embedding-ada-002').lower()
            if "qwen" in model_name:
                embedding_size = 4096
            else:
                embedding_size = 1536  # Default for OpenAI models

            try:
                collections = self.client.get_collections()
            except Exception as e:
                # Provide clearer guidance if the request was forbidden
                err_text = str(e)
                if '403' in err_text or 'forbidden' in err_text.lower():
                    logger.warning("Qdrant API returned 403 Forbidden on collection check. This may be a permissions issue, but proceeding with upsert which may still work.")
                    logger.debug(f"Raw error from Qdrant: {err_text}")
                else:
                    logger.error(f"Error fetching collections from Qdrant: {err_text}")
                # Don't fail on 403 - upsert may still work with existing collection
                return
            collection_exists = any(col.name == self.collection_name for col in collections.collections)

            if not collection_exists:
                # Create collection with vector configuration based on the embedding model
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(size=embedding_size, distance=Distance.COSINE),
                )
                logger.info(f"Created Qdrant collection: {self.collection_name} with {embedding_size}-dimensional vectors")
            else:
                logger.info(f"Qdrant collection exists: {self.collection_name}")

                # Check if the existing collection has the correct vector size
                collection_info = self.client.get_collection(self.collection_name)
                if collection_info.config.params.vectors.size != embedding_size:
                    logger.warning(f"Collection vector size mismatch: expected {embedding_size}, got {collection_info.config.params.vectors.size}")
                    logger.warning("You may need to recreate the collection to change the vector size")

        except Exception as e:
            logger.error(f"Error checking/creating Qdrant collection: {e}")
            raise

    async def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of texts using OpenRouter API
        """
        try:
            import requests

            # Check for API key - prefer OpenRouter, fallback to OpenAI
            api_key = settings.openrouter_api_key or settings.openai_api_key
            if not api_key:
                raise Exception("Missing API key: OPENROUTER_API_KEY or OPENAI_API_KEY not set in environment")

            # Using OpenRouter embeddings endpoint
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "http://localhost:8000",
                "X-Title": "RAG Chatbot"
            }

            # Prepare the request for OpenRouter embeddings
            model_name = getattr(settings, 'openai_model', 'openai/text-embedding-ada-002')
            data = {
                "model": model_name,
                "input": texts
            }

            response = requests.post(
                "https://openrouter.ai/api/v1/embeddings",
                headers=headers,
                json=data
            )

            if response.status_code != 200:
                raise Exception(f"Error from OpenRouter API: {response.status_code} - {response.text}")

            response_data = response.json()
            return [item['embedding'] for item in response_data['data']]
        except Exception as e:
            logger.error(f"Error generating embeddings: {e}")
            raise

    async def store_book_content_chunks(self, chunks: List[BookContentChunkCreate]) -> bool:
        """
        Store multiple book content chunks and their embeddings in Qdrant with retry logic
        """
        import uuid
        
        try:
            batch_size = 5  # Smaller batches for stability
            total_chunks = len(chunks)
            max_retries = 3
            
            logger.info(f"Starting to store {total_chunks} content chunks in batches of {batch_size}")

            for i in range(0, total_chunks, batch_size):
                batch = chunks[i:i + batch_size]
                batch_num = (i // batch_size) + 1
                texts = [chunk.content for chunk in batch]

                # Generate embeddings with retry
                retry_count = 0
                embeddings = None
                while retry_count < max_retries and embeddings is None:
                    try:
                        embeddings = await self.generate_embeddings(texts)
                    except Exception as e:
                        retry_count += 1
                        if retry_count < max_retries:
                            wait_time = 2 ** retry_count
                            logger.warning(f"Embedding retry {retry_count}/{max_retries} in {wait_time}s: {e}")
                            await asyncio.sleep(wait_time)
                        else:
                            raise

                # Prepare points
                points = []
                for j, chunk in enumerate(batch):
                    payload = {
                        "content": chunk.content,
                        "document_id": chunk.document_id,
                        "chunk_id": str(chunk.chunk_id) if hasattr(chunk, 'chunk_id') else f"{chunk.document_id}_{i+j}",
                        "metadata": chunk.metadata or {}
                    }
                    point_id = str(uuid.uuid4())
                    points.append(models.PointStruct(id=point_id, vector=embeddings[j], payload=payload))

                # Upsert with retry
                retry_count = 0
                stored = False
                while retry_count < max_retries and not stored:
                    try:
                        self.client.upsert(collection_name=self.collection_name, points=points)
                        stored = True
                        logger.info(f"Stored batch {batch_num} ({len(batch)} chunks)")
                    except Exception as e:
                        retry_count += 1
                        if retry_count < max_retries:
                            wait_time = 2 ** retry_count
                            logger.warning(f"Upsert retry {retry_count}/{max_retries} in {wait_time}s: {e}")
                            await asyncio.sleep(wait_time)
                        else:
                            raise

            logger.info(f"Successfully stored all {total_chunks} chunks")
            return True
        except Exception as e:
            logger.error(f"Error storing chunks: {e}")
            return False

    async def store_single_chunk(self,
                                chunk_id: str,
                                content: str,
                                document_id: str,
                                metadata: Optional[Dict[str, Any]] = None) -> bool:
        """
        Store a single chunk content and its embedding in Qdrant
        """
        try:
            # Generate embedding for the content
            embeddings = await self.generate_embeddings([content])
            embedding_vector = embeddings[0]

            # Prepare metadata
            payload = {
                "content": content,
                "document_id": document_id,
                "chunk_id": chunk_id
            }
            if metadata:
                payload.update(metadata)

            # Store in Qdrant
            self.client.upsert(
                collection_name=self.collection_name,
                points=[
                    models.PointStruct(
                        id=chunk_id,
                        vector=embedding_vector,
                        payload=payload
                    )
                ]
            )
            return True
        except Exception as e:
            logger.error(f"Error storing embedding: {e}")
            return False

    async def search_similar(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Search for similar content based on the query
        """
        try:
            # Generate embedding for the query
            query_embeddings = await self.generate_embeddings([query])
            query_vector = query_embeddings[0]

            # Search in Qdrant
            search_result = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                limit=limit
            )

            # Format results
            results = []
            for hit in search_result:
                result = {
                    "chunk_id": hit.id,
                    "content": hit.payload.get("content", ""),
                    "document_id": hit.payload.get("document_id", ""),
                    "score": hit.score,
                    "metadata": hit.payload
                }
                results.append(result)

            return results
        except Exception as e:
            logger.error(f"Error searching similar content: {e}")
            return []

    def delete_embeddings(self, chunk_ids: List[str]) -> bool:
        """
        Delete embeddings by chunk IDs
        """
        try:
            self.client.delete(
                collection_name=self.collection_name,
                points_selector=models.PointIdsList(
                    points=chunk_ids
                )
            )
            return True
        except Exception as e:
            logger.error(f"Error deleting embeddings: {e}")
            return False