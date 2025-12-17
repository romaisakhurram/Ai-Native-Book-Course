"""
Script to index book content into the vector database (Qdrant)
"""
import asyncio
import sys
import os
from pathlib import Path

# Add the project root and backend to the path so we can import our modules
project_root = Path(__file__).parent
backend_path = project_root / "backend"
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(backend_path))

# Import backend modules
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

def main():
    import argparse

    parser = argparse.ArgumentParser(description='Index book content into the vector database')
    parser.add_argument('--source-path', required=True, help='Path to the directory containing markdown files')

    args = parser.parse_args()

    # Verify the source path exists
    if not os.path.exists(args.source_path):
        print(f"Error: Source path '{args.source_path}' does not exist")
        sys.exit(1)

    # Run the indexing
    success = asyncio.run(index_book_content(args.source_path))

    if success:
        print("Indexing completed successfully!")
        sys.exit(0)
    else:
        print("Indexing failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()