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
    Test connection to Qdrant and check for existing collections and points
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
            print(f"\n[SUCCESS] Connected to Qdrant collection: {settings.qdrant_collection_name}")
            print(f"Points count: {collection_info.points_count}")
            print(f"Config: {collection_info.config}")
            
            # Get detailed collection info
            print(f"\n[INFO] Detailed Collection Info:")
            print(f"   Status: {collection_info.status}")
            print(f"   Vector Size: {collection_info.config.params.vectors.size}")
            print(f"   Distance: {collection_info.config.params.vectors.distance}")

            # Check a sample of the points if any exist
            if collection_info.points_count > 0:
                print(f"\n[INFO] Sample points in the collection (first 3):")
                scroll_result = embedding_service.client.scroll(
                    collection_name=settings.qdrant_collection_name,
                    limit=3,  # Just get first 3 points
                )

                for idx, point in enumerate(scroll_result[0][:3]):
                    payload = point.payload
                    print(f"\nPoint {idx+1}:")
                    print(f"  ID: {point.id}")
                    print(f"  Document ID: {payload.get('document_id', 'N/A')}")
                    print(f"  Chunk ID: {payload.get('chunk_id', 'N/A')}")
                    print(f"  Content preview: {payload.get('content', '')[:100]}...")

                    # Check the vector size
                    if hasattr(point, 'vector') and point.vector:
                        print(f"  Vector size: {len(point.vector) if hasattr(point.vector, '__len__') else 'N/A'}")
                    else:
                        print("  Vector: Not accessible in preview")

                    # Check metadata
                    if 'metadata' in payload:
                        print(f"  Metadata: {payload['metadata']}")

                print(f"\n[SUCCESS] Sample verification completed for {len(scroll_result[0][:3])} points")
            else:
                print("\n[ERROR] No points found in the collection!")
                print("This could mean:")
                print("  1. The embedding process didn't store the points properly")
                print("  2. There was an issue during the upsert operation")

        except Exception as e:
            print(f"\n[ERROR] Error accessing collection '{settings.qdrant_collection_name}': {e}")
            print("This might mean:")
            print("  - Collection doesn't exist")
            print("  - Incorrect API key or URL")
            print("  - Network connectivity issue")
            import traceback
            traceback.print_exc()

        return True

    except ImportError as e:
        print(f"[ERROR] Error importing modules: {e}")
        return False
    except Exception as e:
        print(f"[ERROR] Error connecting to Qdrant: {e}")
        print("This might be due to:")
        print("  - Missing environment variables (QDRANT_URL, QDRANT_API_KEY)")
        print("  - Invalid API keys or URLs")
        print("  - Network connectivity issues")
        import traceback
        traceback.print_exc()
        return False

async def main():
    print("="*60)
    print("QDRANT CONNECTION AND EMBEDDINGS VERIFICATION")
    print("="*60)

    success = await test_qdrant_connection()

    if success:
        print("\n[SUCCESS] Qdrant verification completed")
    else:
        print("\n[ERROR] Qdrant verification failed")

if __name__ == "__main__":
    asyncio.run(main())