"""
Script to test Qdrant connection and check if embeddings are present
"""
import asyncio
import sys
import os
from pathlib import Path

# Add the backend directory to the Python path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

async def test_qdrant_connection():
    """
    Test connection to Qdrant and check for existing collections
    """
    try:
        # Import the embedding service which handles Qdrant connection
        from backend.services.embedding_service import EmbeddingService
        from backend.config.settings import settings
        
        print("Connecting to Qdrant...")
        print(f"Qdrant URL: {settings.qdrant_url}")
        print(f"Collection name: {settings.qdrant_collection_name}")
        
        # Initialize the embedding service (this connects to Qdrant)
        embedding_service = EmbeddingService()
        
        # Get collection info
        try:
            collection_info = embedding_service.client.get_collection(settings.qdrant_collection_name)
            print(f"\n✅ Connected to Qdrant collection: {settings.qdrant_collection_name}")
            print(f"Points count: {collection_info.points_count}")
            print(f"Vectors count: {collection_info.vectors_count}")
            print(f"Config: {collection_info.config}")
            
            # If there are points in the collection, check a few of them
            if collection_info.points_count > 0:
                print("\nSample points in the collection:")
                # Retrieve a few points to verify content
                scroll_result = embedding_service.client.scroll(
                    collection_name=settings.qdrant_collection_name,
                    limit=3,  # Just get first 3 points
                )
                
                for idx, point in enumerate(scroll_result[0][:3]):
                    payload = point.payload
                    print(f"\nPoint {idx+1}:")
                    print(f"  ID: {point.id}")
                    print(f"  Document ID: {payload.get('document_id', 'N/A')}")
                    print(f"  Content preview: {payload.get('content', '')[:100]}...")
                    
            else:
                print("\nNo points found in the collection.")
                print("This means either:")
                print("  1. No embeddings have been sent to Qdrant yet")
                print("  2. The embedding process failed")
                
        except Exception as e:
            print(f"\n❌ Error accessing collection '{settings.qdrant_collection_name}': {e}")
            print("This might mean:")
            print("  - Collection doesn't exist yet (will be created on first insertion)")
            print("  - Incorrect API key or URL")
            print("  - Network connectivity issue")
        
        return True
        
    except ImportError as e:
        print(f"❌ Error importing modules: {e}")
        return False
    except Exception as e:
        print(f"❌ Error connecting to Qdrant: {e}")
        print("This might be due to:")
        print("  - Missing environment variables (QDRANT_URL, QDRANT_API_KEY)")
        print("  - Invalid API keys or URLs")
        print("  - Network connectivity issues")
        return False

async def main():
    print("="*60)
    print("QDRANT CONNECTION AND EMBEDDINGS TEST")
    print("="*60)
    
    success = await test_qdrant_connection()
    
    if success:
        print("\n✅ Qdrant test completed")
    else:
        print("\n❌ Qdrant test failed")
        print("\nTo properly set up the embedding process:")
        print("1. Make sure you have a .env file with QDRANT_URL and QDRANT_API_KEY")
        print("2. Run this from the backend directory: python -c \"exec(open('test_qdrant.py').read())\"")
        
if __name__ == "__main__":
    asyncio.run(main())