#!/usr/bin/env python3
"""
RAG Chatbot Content Embedding Script

This script embeds your book content into Qdrant for the RAG system.
To run this script, you need to provide real API keys.
"""

import os
import asyncio
from pathlib import Path
import sys

sys.path.insert(0, './backend')
from dotenv import load_dotenv
load_dotenv()

async def main():
    print("📚 RAG Chatbot - Content Embedding Process")
    print("="*50)
    
    # Check if the required files exist
    if not os.path.exists("./frontend/docs"):
        print("❌ Error: frontend/docs directory does not exist!")
        print("   This directory should contain your book's Markdown files.")
        return False
    
    if not os.path.exists("./backend"):
        print("❌ Error: backend directory does not exist!")
        print("   Make sure you're running this from the project root.")
        return False
    
    docs_path = Path("./frontend/docs")
    md_files = list(docs_path.rglob("*.md"))
    
    if not md_files:
        print("❌ No Markdown files found in frontend/docs/")
        print("   Please add your book content as .md files to this directory.")
        return False
    
    print(f"📁 Found {len(md_files)} Markdown files to process:")
    for file in md_files[:5]:  # Show first 5 files
        print(f"   • {file}")
    if len(md_files) > 5:
        print(f"   ... and {len(md_files) - 5} more files")
    
    print("\n🔐 API Key Configuration Required:")
    print("   Before running the embedding, you need real API keys:")
    print("   • Qdrant Cloud URL and API Key")
    print("   • OpenRouter API Key")
    
    # Check for environment variables
    qdrant_url = os.getenv('QDRANT_URL')
    qdrant_key = os.getenv('QDRANT_API_KEY')
    openrouter_key = os.getenv('OPENROUTER_API_KEY')
    
    print(f"\n📋 Current environment setup:")
    print(f"   QDRANT_URL: {'SET' if qdrant_url else 'NOT SET'}")
    print(f"   QDRANT_API_KEY: {'SET' if qdrant_key else 'NOT SET'}")
    print(f"   OPENROUTER_API_KEY: {'SET' if openrouter_key else 'NOT SET'}")
    
    if not (qdrant_url and qdrant_key and openrouter_key):
        print("\n⚠️  Missing API keys. You need to set them:")
        print("\n   Method 1: Create a .env file in backend/:")
        print("     QDRANT_URL=your_actual_qdrant_url")
        print("     QDRANT_API_KEY=your_actual_qdrant_api_key") 
        print("     OPENROUTER_API_KEY=your_actual_openrouter_api_key")
        
        print("\n   Method 2: Set environment variables:")
        print("     export QDRANT_URL=your_actual_qdrant_url")
        print("     export QDRANT_API_KEY=your_actual_qdrant_api_key")
        print("     export OPENROUTER_API_KEY=your_actual_openrouter_api_key")
        
        print("\n   After setting up the API keys, run:")
        print("   python -c \"exec(open('embed_content.py').read())\"")
        return False
    
    print("\n🚀 Starting the embedding process...")
    
    try:
        # Import and run the actual embedding
        from backend.services.content_processor import ContentProcessor
        from backend.services.embedding_service import EmbeddingService
        from backend.config.settings import settings
        
        print(f"🌐 Connecting to Qdrant: {settings.qdrant_url}")
        print(f"🏷️  Collection: {settings.qdrant_collection_name}")
        
        # Initialize services
        content_processor = ContentProcessor()
        embedding_service = EmbeddingService()
        
        print("✅ Services connected successfully")
        
        # Process the content
        print("\n📝 Processing content...")
        chunks = content_processor.process_directory("./frontend/docs")
        print(f"✅ Processed {len(chunks)} content chunks")
        
        if len(chunks) == 0:
            print("⚠️  No content found to embed")
            return False
        
        # Store in Qdrant
        print(f"\n🧠 Generating and storing embeddings (this may take a few minutes)...")
        success = await embedding_service.store_book_content_chunks(chunks)
        
        if success:
            print(f"\n🎉 SUCCESS: {len(chunks)} content chunks embedded!")
            print("✅ Your book content is now in Qdrant and ready for the RAG chatbot")
            print("🤖 You can now ask questions and get answers based on your book content")
            
            # Show collection stats
            try:
                collection_info = embedding_service.client.get_collection(settings.qdrant_collection_name)
                print(f"📊 Collection stats: {collection_info.points_count} vectors stored")
            except Exception as e:
                print(f"ℹ️  Could not get detailed stats: {e}")
                
            return True
        else:
            print("❌ Embedding failed - check your network connection and API keys")
            return False
            
    except Exception as e:
        print(f"❌ Error during embedding: {e}")
        import traceback
        traceback.print_exc()
        return False

# Allow this file to be executed as a script
if __name__ == "__main__":
    import asyncio
    result = asyncio.run(main())
    sys.exit(0 if result else 1)