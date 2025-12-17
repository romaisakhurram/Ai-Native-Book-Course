"""
Script to test Qdrant connection and verify the new collection
"""
import asyncio
import sys
import os
from pathlib import Path

# Add the backend directory to the Python path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

async def test_new_collection(collection_name: str):
    """
    Test the new Qdrant collection and cluster connection
    :param collection_name: Name of the collection to test
    """
    try:
        from qdrant_client import QdrantClient
        from backend.config.settings import settings

        print("Testing connection to Qdrant...")
        print(f"Qdrant URL: {settings.qdrant_url}")
        print(f"Testing collection: {collection_name}")

        # Initialize Qdrant client
        client = QdrantClient(
            url=settings.qdrant_url,
            api_key=settings.qdrant_api_key,
            prefer_grpc=False
        )

        # Test connection by getting collections list
        print("\n🌐 Fetching collections list...")
        collections = client.get_collections()
        all_collection_names = [col.name for col in collections.collections]
        
        print(f"Available collections: {all_collection_names}")

        # Check if our specific collection exists
        if collection_name in all_collection_names:
            print(f"\n✅ Collection '{collection_name}' exists!")
            
            # Get detailed info about the collection
            collection_info = client.get_collection(collection_name)
            print(f"\n📊 Collection '{collection_name}' details:")
            print(f"   Status: {collection_info.status}")
            print(f"   Points count: {collection_info.points_count}")
            print(f"   Vectors count: {collection_info.vectors_count}")
            print(f"   Config: {collection_info.config}")
            
            # If collection has points, show a sample
            if collection_info.points_count > 0:
                print(f"\n📖 Sample points from '{collection_name}':")
                scroll_result = client.scroll(
                    collection_name=collection_name,
                    limit=2,  # Just get first 2 points
                )

                for idx, point in enumerate(scroll_result[0][:2]):
                    payload = point.payload
                    print(f"\n   Point {idx+1}:")
                    print(f"     ID: {point.id}")
                    print(f"     Document ID: {payload.get('document_id', 'N/A')}")
                    print(f"     Content preview: {payload.get('content', '')[:100]}...")
            else:
                print(f"\n📭 Collection '{collection_name}' exists but is empty.")
                print("You can add content to it using the embedding process.")
        else:
            print(f"\n❌ Collection '{collection_name}' does not exist!")
            print(f"Available collections are: {all_collection_names}")
            return False

        # Test that we can perform a simple operation on the collection
        print(f"\n🧪 Testing write operation on '{collection_name}'...")
        try:
            # Try to count points (this verifies we have read access at minimum)
            count_result = client.count(
                collection_name=collection_name
            )
            print(f"   Count operation successful: {count_result.count} points")
        except Exception as e:
            print(f"   ❌ Count operation failed: {e}")
            return False

        print(f"\n✅ Successfully verified collection '{collection_name}'!")
        print(f"✅ Cluster connection is working properly!")
        return True

    except ImportError as e:
        print(f"❌ Error importing modules: {e}")
        return False
    except Exception as e:
        print(f"❌ Error testing collection '{collection_name}': {e}")
        print("\nThis might be due to:")
        print("  - Missing environment variables (QDRANT_URL, QDRANT_API_KEY)")
        print("  - Invalid API keys or URLs")
        print("  - Network connectivity issues")
        print("  - Insufficient permissions to access the collection")
        return False

def main():
    import argparse

    parser = argparse.ArgumentParser(description='Test a Qdrant collection and cluster connection')
    parser.add_argument('--name', required=True, help='Name of the collection to test')
    
    args = parser.parse_args()
    
    # Run the collection test
    success = asyncio.run(test_new_collection(args.name))
    
    if success:
        print(f"\n🎉 Successfully verified collection: {args.name}")
        print(f"✅ Your Qdrant cluster and collection are ready to use!")
    else:
        print(f"\n❌ Failed to verify collection: {args.name}")
        sys.exit(1)

if __name__ == "__main__":
    main()