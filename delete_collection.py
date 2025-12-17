"""
Script to delete an existing Qdrant collection to recreate it with correct vector dimensions
"""
import sys
import os
from pathlib import Path

# Add the backend directory to the Python path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

def delete_collection(collection_name: str):
    """
    Delete a Qdrant collection
    :param collection_name: Name of the collection to delete
    """
    try:
        from qdrant_client import QdrantClient
        from backend.config.settings import settings
        
        print(f"Attempting to connect to Qdrant...")
        print(f"URL: {settings.qdrant_url}")
        print(f"API Key present: {'Yes' if settings.qdrant_api_key else 'No'}")
        print(f"Target collection: {collection_name}")
        
        # Initialize Qdrant client
        client = QdrantClient(
            url=settings.qdrant_url,
            api_key=settings.qdrant_api_key,
            prefer_grpc=False
        )
        
        # Check if collection exists
        collections = client.get_collections()
        collection_exists = any(col.name == collection_name for col in collections.collections)
        
        if collection_exists:
            print(f"\n🗑️  Deleting existing collection '{collection_name}'...")
            client.delete_collection(collection_name)
            print(f"✅ Collection '{collection_name}' deleted successfully.")
            print(f"📊 You can now run the embedding process again to recreate the collection with correct dimensions.")
        else:
            print(f"\n⚠️  Collection '{collection_name}' does not exist!")
            print(f"Available collections are: {[col.name for col in collections.collections]}")
            return False

        return True

    except ImportError as e:
        print(f"❌ Error importing modules: {e}")
        return False
    except Exception as e:
        print(f"❌ Error deleting collection: {e}")
        print("\nThis might be due to:")
        print("  - Missing environment variables (QDRANT_URL, QDRANT_API_KEY)")
        print("  - Invalid API keys or URLs")
        print("  - Network connectivity issues")
        print("  - Insufficient permissions to delete the collection")
        return False

if __name__ == "__main__":
    from backend.config.settings import settings
    collection_name = settings.qdrant_collection_name
    
    print(f"Deleting collection: {collection_name}")
    success = delete_collection(collection_name)
    
    if success:
        print(f"\n🎉 Successfully deleted collection: {collection_name}")
        print(f"📖 You can now run the embedding process again")
        print(f"📖 The embedding process will recreate the collection with correct vector dimensions")
    else:
        print(f"\n❌ Failed to delete collection: {collection_name}")
        exit(1)