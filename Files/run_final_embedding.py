#!/usr/bin/env python3
"""
FINAL EMBEDDING SCRIPT - WITH YOUR ACTUAL API KEYS
"""
import os
import asyncio
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, './backend')

def run_embedding():
    print("🚀 RAG CHATBOT - FINAL EMBEDDING PROCESS")
    print("="*50)
    
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv('./backend/.env')
    
    # Verify API keys are present
    qdrant_url = os.getenv('QDRANT_URL')
    qdrant_api_key = os.getenv('QDRANT_API_KEY')
    openrouter_api_key = os.getenv('OPENROUTER_API_KEY')
    
    if not all([qdrant_url, qdrant_api_key, openrouter_api_key]):
        print("❌ ERROR: API keys are not properly set in the environment")
        return False
    
    print("✅ API KEYS VERIFIED")
    print(f"Qdrant URL: {qdrant_url}")
    print(f"Has Qdrant Key: {len(qdrant_api_key) > 10}")
    print(f"Has OpenRouter Key: {len(openrouter_api_key) > 10}")
    
    # Check source content
    source_path = "frontend/docs"
    if not os.path.exists(source_path):
        print(f"❌ Source path does not exist: {source_path}")
        return False
    
    docs_dir = Path(source_path)
    md_files = list(docs_dir.rglob("*.md"))
    print(f"📚 Found {len(md_files)} Markdown files to embed")
    
    if len(md_files) == 0:
        print("⚠️  No Markdown files found in frontend/docs/")
        return False
    
    try:
        # Import required modules
        from backend.services.content_processor import ContentProcessor
        from backend.services.embedding_service import EmbeddingService
        from backend.config.settings import settings
        
        print(f"\n🎯 Target Collection: {settings.qdrant_collection_name}")
        print(f"🌐 Qdrant Endpoint: {settings.qdrant_url}")
        
        # Initialize services
        print("\n🔧 Initializing Content Processor...")
        content_processor = ContentProcessor()
        print("✅ Content Processor initialized")
        
        print("\n🔧 Connecting to Qdrant (this may take a moment)...")
        embedding_service = EmbeddingService()
        print("✅ Successfully connected to Qdrant!")
        
        # Process content
        print(f"\n📖 Processing {len(md_files)} markdown files...")
        chunks = content_processor.process_directory(source_path)
        print(f"✅ Processed {len(chunks)} content chunks")
        
        if len(chunks) > 0:
            print(f"\n💾 STORING {len(chunks)} CHUNKS IN QDRANT...")
            print("(This may take a few minutes)")
            
            # Store chunks in Qdrant
            success = asyncio.run(embedding_service.store_book_content_chunks(chunks))
            
            if success:
                print(f"\n🎉 SUCCESS: {len(chunks)} chunks stored in Qdrant!")
                
                # Get collection stats
                try:
                    collection_info = embedding_service.client.get_collection(settings.qdrant_collection_name)
                    print(f"📊 Final Stats: {collection_info.points_count} vectors in collection")
                except Exception as e:
                    print(f"ℹ️  Stats: {e}")
                
                print("\n✨ EMBEDDING COMPLETED SUCCESSFULLY!")
                print("🌟 YOUR CONTENT IS NOW IN QDRANT!")
                print("🤖 The RAG chatbot can now answer questions about your book content!")
                
                return True
            else:
                print("\n❌ FAILED to store content in Qdrant")
                return False
        else:
            print("⚠️  No content chunks to process")
            return False
            
    except Exception as e:
        print(f"❌ Error during embedding: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = run_embedding()
    
    print("\n" + "="*50)
    if success:
        print("🎊 EMBEDDING PROCESS COMPLETED SUCCESSFULLY! 🎊")
        print("Your book content is now stored in Qdrant and ready for the RAG chatbot!")
    else:
        print("💥 EMBEDDING PROCESS FAILED!")
        print("This may be due to network issues or API key validation problems.")
    print("="*50)