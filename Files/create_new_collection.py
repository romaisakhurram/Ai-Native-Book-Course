"""
Script to create a new Qdrant collection with custom settings
"""
import asyncio
import os
import sys
from pathlib import Path

# Add the backend directory to the Python path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

async def create_new_collection(collection_name: str, recreate: bool = False):
    """
    Create a new Qdrant collection
    :param collection_name: Name of the new collection to create
    :param recreate: Whether to recreate the collection if it already exists
    """
    try:
        from qdrant_client import QdrantClient
        from qdrant_client.http import models
        from qdrant_client.http.models import Distance, VectorParams
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
        
        # Check if collection already exists
        collections = client.get_collections()
        collection_exists = any(col.name == collection_name for col in collections.collections)
        
        if collection_exists and not recreate:
            print(f"\n⚠️  Collection '{collection_name}' already exists!")
            print("Use --recreate flag to delete and recreate it.")
            return False
        elif collection_exists and recreate:
            print(f"\n🗑️  Deleting existing collection '{collection_name}'...")
            client.delete_collection(collection_name)
            print(f"✅ Collection '{collection_name}' deleted.")
        
        # Create the new collection with vector configuration
        print(f"\n🆕 Creating new collection '{collection_name}'...")
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(
                size=1536,  # Standard OpenAI embedding size
                distance=Distance.COSINE
            )
        )
        
        print(f"✅ Collection '{collection_name}' created successfully!")
        
        # Verify the collection exists
        collection_info = client.get_collection(collection_name)
        print(f"\n📊 Collection Info:")
        print(f"   Name: {collection_info.config.params.vectors.size}")
        print(f"   Vector Size: {collection_info.config.params.vectors.size}")
        print(f"   Distance: {collection_info.config.params.vectors.distance}")
        print(f"   Points Count: {collection_info.points_count}")
        
        return True

    except ImportError as e:
        print(f"❌ Error importing modules: {e}")
        return False
    except Exception as e:
        print(f"❌ Error creating collection: {e}")
        print("\nThis might be due to:")
        print("  - Missing environment variables (QDRANT_URL, QDRANT_API_KEY)")
        print("  - Invalid API keys or URLs")
        print("  - Network connectivity issues")
        print("  - Insufficient permissions on your Qdrant cluster")
        return False

def main():
    import argparse

    parser = argparse.ArgumentParser(description='Create a new Qdrant collection')
    parser.add_argument('--name', required=True, help='Name of the new collection to create')
    parser.add_argument('--recreate', action='store_true', help='Recreate collection if it already exists')
    
    args = parser.parse_args()
    
    # Run the collection creation
    success = asyncio.run(create_new_collection(args.name, args.recreate))
    
    if success:
        print(f"\n🎉 Successfully created collection: {args.name}")
        print(f"📖 To use this collection, update your QDRANT_COLLECTION_NAME in your .env file")
    else:
        print(f"\n❌ Failed to create collection: {args.name}")
        sys.exit(1)

if __name__ == "__main__":
    main()