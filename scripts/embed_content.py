"""
Simple script to run the embedding process
"""
import asyncio
import sys
import os
from pathlib import Path

# Add the backend directory to Python path
sys.path.insert(0, './backend')

# Import backend modules
from backend.services.content_processor import ContentProcessor
from backend.services.embedding_service import EmbeddingService
from backend.config.settings import settings

async def run_embedding(source_path):
    print(f"Starting to index content from: {source_path}")
    
    # Initialize the services
    content_processor = ContentProcessor()
    embedding_service = EmbeddingService()
    
    print("Connected to Qdrant successfully")
    
    # Process the directory to get content chunks
    print("Processing markdown files...")
    chunks = content_processor.process_directory(source_path)
    print(f"Processed {len(chunks)} content chunks")
    
    # Store all chunks in Qdrant
    print("Storing embeddings in Qdrant...")
    success = await embedding_service.store_book_content_chunks(chunks)
    
    if success:
        print(f"Successfully stored {len(chunks)} chunks in Qdrant collection '{settings.qdrant_collection_name}'")
    else:
        print("Failed to store chunks in Qdrant")
    
    return success

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/embed_content.py <source_path>")
        print("Example: python scripts/embed_content.py frontend/docs")
        sys.exit(1)
    
    source_path = sys.argv[1]
    
    # Check if source path exists
    if not os.path.exists(source_path):
        print(f"Error: Source path '{source_path}' does not exist")
        sys.exit(1)
    
    # Run the embedding process
    print("\nStarting the embedding process...")
    success = asyncio.run(run_embedding(source_path))
    
    if success:
        print("\n✅ Embedding completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Embedding failed!")
        sys.exit(1)