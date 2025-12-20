import logging
from typing import List, Dict, Any
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
import uuid

logger = logging.getLogger(__name__)

class QdrantService:
    """
    Service to handle vector storage and search using Qdrant
    """
    
    def __init__(self, host: str = "localhost", port: int = 6333, collection_name: str = "book_content"):
        self.host = host
        self.port = port
        self.collection_name = collection_name
        self.client = QdrantClient(host=host, port=port)
        self._initialize_collection()
    
    def _initialize_collection(self):
        """
        Initialize the Qdrant collection if it doesn't exist
        """
        try:
            # Check if collection exists
            collections = self.client.get_collections()
            collection_exists = any(col.name == self.collection_name for col in collections.collections)
            
            if not collection_exists:
                # Create collection with vector configuration
                self.client.recreate_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(
                        size=1536,  # Standard embedding size
                        distance=Distance.COSINE
                    )
                )
                logger.info(f"Created Qdrant collection: {self.collection_name}")
            else:
                logger.info(f"Using existing Qdrant collection: {self.collection_name}")
                
        except Exception as e:
            logger.error(f"Error initializing Qdrant collection: {str(e)}")
            raise
    
    def add_content(self, content: str, title: str = "", url: str = "", metadata: Dict[str, Any] = None) -> str:
        """
        Add content to the vector store with embeddings
        """
        try:
            # This method will be implemented with the embedding model when needed
            # For now, we'll just return a placeholder
            content_id = str(uuid.uuid4())
            
            # Prepare payload
            payload = {
                "content": content,
                "title": title,
                "url": url,
                "metadata": metadata or {}
            }
            
            # In a real implementation, we would generate embeddings here
            # For now, using a placeholder vector
            embedding = [0.0] * 1536  # Placeholder embedding
            
            # Insert into Qdrant
            points = [
                PointStruct(
                    id=content_id,
                    vector=embedding,
                    payload=payload
                )
            ]
            
            self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )
            
            logger.info(f"Added content to Qdrant with ID: {content_id}")
            return content_id
            
        except Exception as e:
            logger.error(f"Error adding content to Qdrant: {str(e)}")
            raise
    
    def search(self, query: str, limit: int = 5) -> List[Any]:
        """
        Search for content in the vector store
        """
        try:
            # In a real implementation, we would generate query embeddings here
            # For now, using a placeholder vector
            query_embedding = [0.0] * 1536  # Placeholder embedding
            
            # Perform search in Qdrant
            search_result = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=limit
            )
            
            logger.info(f"Found {len(search_result)} results for query: {query[:50]}...")
            return search_result
            
        except Exception as e:
            logger.error(f"Error searching Qdrant: {str(e)}")
            raise
    
    def batch_add_content(self, contents: List[Dict[str, Any]]) -> List[str]:
        """
        Add multiple content items to the vector store
        """
        try:
            points = []
            ids = []
            
            for content_item in contents:
                content = content_item.get("content", "")
                title = content_item.get("title", "")
                url = content_item.get("url", "")
                metadata = content_item.get("metadata", {})
                
                # Create unique ID
                content_id = str(uuid.uuid4())
                ids.append(content_id)
                
                # Prepare payload
                payload = {
                    "content": content,
                    "title": title,
                    "url": url,
                    "metadata": metadata
                }
                
                # Placeholder embedding
                embedding = [0.0] * 1536
                
                # Create point
                point = PointStruct(
                    id=content_id,
                    vector=embedding,
                    payload=payload
                )
                
                points.append(point)
            
            # Batch insert
            self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )
            
            logger.info(f"Added {len(points)} content items to Qdrant")
            return ids
            
        except Exception as e:
            logger.error(f"Error batch adding content to Qdrant: {str(e)}")
            raise