"""
Debug script to understand the Qdrant client API structure
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

async def debug_qdrant_client():
    """
    Debug the Qdrant client to understand its API structure
    """
    print("Debugging Qdrant client API structure...")
    
    # Initialize the embedding service
    embedding_service = EmbeddingService()
    client = embedding_service.client
    
    print(f"Qdrant client type: {type(client)}")
    print(f"Qdrant client attributes: {[attr for attr in dir(client) if not attr.startswith('_')]}")
    
    # Check for HTTP API
    if hasattr(client, 'http'):
        print(f"\nHTTP API available:")
        print(f"  http type: {type(client.http)}")
        print(f"  http attributes: {[attr for attr in dir(client.http) if not attr.startswith('_')]}")
        
        if hasattr(client.http, 'points_api'):
            print(f"\npoints_api available:")
            print(f"  points_api type: {type(client.http.points_api)}")
            print(f"  points_api attributes: {[attr for attr in dir(client.http.points_api) if 'search' in attr.lower()]}")
    
    # Check for GRPC API
    if hasattr(client, 'grpc_points_api'):
        print(f"\ngrpc_points_api available: {type(client.grpc_points_api)}")
    
    # Check all search-related methods
    search_methods = [method for method in dir(client) if 'search' in method.lower()]
    print(f"\nAll search-related methods: {search_methods}")
    
    # Let's try to understand the search_matrix_offsets method which is available
    if 'search_matrix_offsets' in search_methods:
        matrix_offsets_method = getattr(client, 'search_matrix_offsets')
        print(f"\nsearch_matrix_offsets signature: {matrix_offsets_method}")
        print(f"Type: {type(matrix_offsets_method)}")

if __name__ == "__main__":
    asyncio.run(debug_qdrant_client())