"""
Test script to verify content in Qdrant and test search functionality
"""
import asyncio
import sys
import os

# Add the backend directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from services.embedding_service import EmbeddingService
from config.settings import settings
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_content_and_search():
    """
    Test the content in Qdrant and search functionality
    """
    print("Testing content in Qdrant and search functionality...")
    
    # Initialize the embedding service
    embedding_service = EmbeddingService()
    
    # First, let's count how many points are in the collection
    try:
        collection_info = embedding_service.client.get_collection(settings.qdrant_collection_name)
        print(f"Collection '{settings.qdrant_collection_name}' has {collection_info.points_count} points")
        
        if collection_info.points_count == 0:
            print("ERROR: No points found in the collection!")
            return
    except Exception as e:
        print(f"Error getting collection info: {e}")
        return
    
    # Let's get a sample of points to see what's stored
    try:
        # Get first 3 points to inspect
        sample_points_response = embedding_service.client.scroll(
            collection_name=settings.qdrant_collection_name,
            limit=3
        )
        
        print(f"\nSample of stored content (first 3 entries):")
        
        # Handle different Qdrant client response formats
        try:
            # Newer format: response with points attribute
            sample_points = sample_points_response.points
        except AttributeError:
            # Older format: response is a tuple (points_list, next_offset)
            sample_points = sample_points_response[0]
        
        for i, point in enumerate(sample_points):
            try:
                # For newer format where point is a PointStruct
                point_id = point.id
                payload = point.payload
            except AttributeError:
                # For older format where point is a dictionary
                point_id = point.get('id', 'unknown') if isinstance(point, dict) else 'unknown'
                payload = point.get('payload', {}) if isinstance(point, dict) else {}
            
            print(f"Point {i+1}:")
            print(f"  ID: {point_id}")
            print(f"  Content (first 100 chars): {payload.get('content', '')[:100]}...")
            print(f"  Document ID: {payload.get('document_id', 'N/A')}")
            print(f"  Metadata keys: {list(payload.get('metadata', {}).keys())}")
            print()
    except Exception as e:
        print(f"Error retrieving sample points: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Now let's test a search with a sample query
    sample_queries = [
        "What are AI Native applications?",
        "Explain transformer architecture",
        "How does RAG work?",
        "What are embeddings?"
    ]
    
    print("Testing search functionality with sample queries:")
    for query in sample_queries:
        print(f"\nQuery: '{query}'")
        try:
            results = await embedding_service.search_similar(query, limit=2)
            print(f"Found {len(results)} results")
            for i, result in enumerate(results):
                print(f"  Result {i+1}: Score={result.get('score', 'N/A')}, Content='{result.get('content', '')[:100]}...'")
        except Exception as e:
            print(f"  Error during search: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_content_and_search())