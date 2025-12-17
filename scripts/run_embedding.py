"""
Script to index book content into the vector database (Qdrant)
This is the main script that should be run to embed your book content.
"""
import asyncio
import sys
import os
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Add the backend directory to the Python path
backend_path = project_root / "backend"
sys.path.insert(0, str(backend_path))

# Import the backend modules after setting up the path
def run_embedding():
    # Import modules after ensuring proper path setup
    from backend.services.content_processor import ContentProcessor
    from backend.services.embedding_service import EmbeddingService
    from backend.models.schemas import BookContentChunkCreate
    from backend.config.settings import settings
    
    async def index_book_content(source_path: str):
        """
        Index all markdown content from the source path into Qdrant
        :param source_path: Path to the directory containing markdown files
        """
        print(f"Starting to index content from: {source_path}")
        
        # Initialize the services
        content_processor = ContentProcessor()
        embedding_service = EmbeddingService()
        
        # Validate that we can connect to Qdrant (this happens in embedding_service initialization)
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
    
    # Get the source path from command line arguments
    if len(sys.argv) < 2:
        print("Usage: python -c 'exec(open(\"scripts/run_embedding.py\").read())' <source_path>")
        print("Example: python -c 'exec(open(\"scripts/run_embedding.py\").read())' \"frontend/docs\"")
        source_path = input("Enter the path to your markdown files: ").strip()
    else:
        source_path = sys.argv[1]
    
    # Check if source path exists
    if not os.path.exists(source_path):
        print(f"Error: Source path '{source_path}' does not exist")
        sys.exit(1)
    
    # Run the indexing
    print("\nStarting the embedding process...")
    success = asyncio.run(index_book_content(source_path))
    
    if success:
        print("\n✅ Embedding completed successfully!")
        return True
    else:
        print("\n❌ Embedding failed!")
        return False

if __name__ == "__main__":
    run_embedding()