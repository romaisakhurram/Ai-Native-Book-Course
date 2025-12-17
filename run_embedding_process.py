"""
Script to run the full embedding process for the RAG chatbot
This script handles the embedding of book content into Qdrant
"""
import asyncio
import sys
import os
from pathlib import Path

# Add the backend directory to the Python path
sys.path.insert(0, './backend')

# Set up dummy environment variables for testing purposes only
os.environ.setdefault('QDRANT_URL', 'https://aa6b9d9c-6094-4978-ab4d-241a6e285813.europe-west3-0.gcp.cloud.qdrant.io:6333')
os.environ.setdefault('QDRANT_API_KEY', 'YOUR_QDRANT_API_KEY_HERE')
os.environ.setdefault('OPENROUTER_API_KEY', 'YOUR_OPENROUTER_API_KEY_HERE')
os.environ.setdefault('NEON_DATABASE_URL', 'YOUR_NEON_DB_URL_HERE')

async def run_full_embedding():
    """Run the complete embedding process"""
    
    print("🚀 Starting RAG Chatbot Content Embedding Process")
    print("=" * 60)
    
    try:
        # Import required modules after setting environment variables
        print("📦 Importing required modules...")
        from backend.services.content_processor import ContentProcessor
        from backend.services.embedding_service import EmbeddingService
        from backend.config.settings import settings
        
        print(f"🌐 Qdrant URL: {settings.qdrant_url}")
        print(f"🏷️  Collection name: {settings.qdrant_collection_name}")
        print(f"🔑 Qdrant API key: {'*' * len(settings.qdrant_api_key) if settings.qdrant_api_key else 'Not set'}")
        
        print("\n🔧 Initializing services...")
        content_processor = ContentProcessor()
        embedding_service = EmbeddingService()
        
        print("✅ Services initialized successfully")
        
        # Define the source path for book content
        source_path = "frontend/docs"
        print(f"\n📖 Source path: {source_path}")
        
        if not os.path.exists(source_path):
            print(f"❌ Error: Source path '{source_path}' does not exist!")
            print("Please make sure the frontend/docs directory exists and contains markdown files.")
            return False
        
        print("\n📝 Processing documents...")
        chunks = content_processor.process_directory(source_path)
        print(f"✅ Processed {len(chunks)} content chunks from {source_path}")
        
        if len(chunks) == 0:
            print("⚠️  Warning: No content was found to process!")
            print("Make sure there are Markdown (.md) files in the frontend/docs directory.")
            return False
        
        print(f"\n🧠 Generating embeddings for {len(chunks)} chunks...")
        print("(This may take a few minutes depending on content size)")
        
        # Store the chunks in Qdrant
        success = await embedding_service.store_book_content_chunks(chunks)
        
        if success:
            print(f"\n🎉 SUCCESS: All {len(chunks)} chunks have been embedded!")
            print("✅ Content has been successfully stored in Qdrant")
            print("🤖 Your RAG chatbot can now answer questions about this content")
            
            # Print some statistics
            print(f"\n📊 Embedding Statistics:")
            print(f"   • Total documents processed: {len([c for c in chunks])}")
            print(f"   • Total content chunks: {len(chunks)}")
            print(f"   • Target collection: {settings.qdrant_collection_name}")
            print(f"   • Content ready for semantic search: ✅")
            
            return True
        else:
            print("❌ FAILED: Could not store embeddings in Qdrant")
            print("This might be due to:")
            print("  - Invalid Qdrant URL or API key")
            print("  - Network connectivity issues")
            print("  - Incorrect Qdrant configuration")
            return False
            
    except Exception as e:
        print(f"❌ ERROR during embedding process: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Preparing to run the embedding process...")
    
    # Check if we have the necessary files
    required_dirs = ["frontend/docs", "backend"]
    missing_dirs = [d for d in required_dirs if not os.path.exists(d)]
    
    if missing_dirs:
        print(f"❌ Missing directories: {missing_dirs}")
        print("Please make sure the project structure is complete.")
        sys.exit(1)
    
    # Check for markdown files in the docs directory
    docs_dir = Path("frontend/docs")
    md_files = list(docs_dir.rglob("*.md"))
    
    if not md_files:
        print("⚠️  No Markdown files found in frontend/docs/")
        print("The system needs markdown files to process and embed.")
    else:
        print(f"📄 Found {len(md_files)} markdown files to embed")
        for i, file in enumerate(md_files[:5]):  # Show first 5 files
            print(f"   {i+1}. {file}")
        if len(md_files) > 5:
            print(f"   ... and {len(md_files) - 5} more files")
    
    print("\n" + "="*60)
    
    # Run the embedding process
    success = asyncio.run(run_full_embedding())
    
    print("\n" + "="*60)
    if success:
        print("🏆 EMBEDDING COMPLETED SUCCESSFULLY!")
        print("Your RAG Chatbot is now ready to answer questions about your book content.")
    else:
        print("💥 EMBEDDING PROCESS FAILED!")
        print("\nTo fix this:")
        print("1. Verify your API keys in the environment")
        print("2. Check your network connection to Qdrant Cloud")
        print("3. Make sure you have valid Markdown files in frontend/docs/")
        print("4. Re-run the embedding process")
    
    print("="*60)