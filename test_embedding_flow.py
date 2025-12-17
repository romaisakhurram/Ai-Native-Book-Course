#!/usr/bin/env python3
"""
Test the complete embedding flow to diagnose issues
"""
import sys
import os
sys.path.insert(0, './backend')

from backend.config.settings import settings
from backend.services.embedding_service import EmbeddingService
from backend.services.content_processor import ContentProcessor
import asyncio

async def test_embedding():
    print("🔍 Testing Embedding Flow")
    print("=" * 60)
    
    # 1. Check environment
    print("\n1️⃣  Checking Environment Variables:")
    print(f"   QDRANT_URL: {settings.qdrant_url}")
    print(f"   QDRANT_API_KEY: {'SET' if settings.qdrant_api_key else 'NOT SET'}")
    print(f"   OPENROUTER_API_KEY: {'SET' if settings.openrouter_api_key else 'NOT SET'}")
    print(f"   Collection Name: {settings.qdrant_collection_name}")
    
    if not settings.qdrant_url or not settings.qdrant_api_key:
        print("\n❌ Missing QDRANT credentials!")
        return False
    
    # 2. Test Qdrant connection
    print("\n2️⃣  Testing Qdrant Connection:")
    try:
        service = EmbeddingService()
        print("   ✅ Qdrant client initialized")
        
        collections = service.client.get_collections()
        print(f"   ✅ Connected to Qdrant. Collections: {[c.name for c in collections.collections]}")
        
        # Check if our collection exists
        try:
            collection_info = service.client.get_collection(settings.qdrant_collection_name)
            print(f"   ✅ Collection '{settings.qdrant_collection_name}' exists")
            print(f"      - Points: {collection_info.points_count}")
            print(f"      - Vector size: {collection_info.config.params.vectors.size}")
        except Exception as e:
            print(f"   ℹ️  Collection not yet created: {e}")
            
    except Exception as e:
        print(f"   ❌ Qdrant connection failed: {e}")
        return False
    
    # 3. Test embedding generation
    print("\n3️⃣  Testing Embedding Generation:")
    try:
        test_texts = ["Hello world", "Testing embeddings", "This is a test"]
        embeddings = await service.generate_embeddings(test_texts)
        print(f"   ✅ Generated {len(embeddings)} embeddings")
        print(f"   ✅ Embedding dimensions: {len(embeddings[0])}")
    except Exception as e:
        print(f"   ❌ Embedding generation failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # 4. Test storing embeddings
    print("\n4️⃣  Testing Storage in Qdrant:")
    try:
        from backend.models.schemas import BookContentChunkCreate
        
        # Create test chunks
        test_chunks = [
            BookContentChunkCreate(
                document_id="test_doc_1",
                content="This is the first test content",
                metadata={"test": True}
            ),
            BookContentChunkCreate(
                document_id="test_doc_2",
                content="This is the second test content",
                metadata={"test": True}
            )
        ]
        
        success = await service.store_book_content_chunks(test_chunks)
        if success:
            print(f"   ✅ Successfully stored {len(test_chunks)} test chunks")
            
            # Verify storage
            collection_info = service.client.get_collection(settings.qdrant_collection_name)
            print(f"   ✅ Collection now contains {collection_info.points_count} total points")
        else:
            print(f"   ❌ Failed to store chunks")
            return False
            
    except Exception as e:
        print(f"   ❌ Storage failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print("\n" + "=" * 60)
    print("✅ All tests passed! Embedding flow is working.")
    return True

if __name__ == "__main__":
    success = asyncio.run(test_embedding())
    sys.exit(0 if success else 1)
