"""
Script to embed book content into the Qdrant vector database
This script processes markdown files and stores their embeddings in Qdrant
"""
import asyncio
import sys
import os

# Add the backend directory to the path so we can import modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.content_processor import ContentProcessor
from services.embedding_service import EmbeddingService
from models.schemas import BookContentChunkCreate


async def embed_book_content(content_dir: str):
    """
    Embed book content from a directory of markdown files into Qdrant
    :param content_dir: Directory containing markdown files to process
    """
    print(f"Processing content from directory: {content_dir}")
    
    # Initialize services
    processor = ContentProcessor(chunk_size=1000, overlap=100)
    embedding_service = EmbeddingService()
    
    # Process all markdown files in the directory
    chunks = processor.process_directory(content_dir)
    
    print(f"Processed {len(chunks)} content chunks from {content_dir}")
    
    # Store chunks in Qdrant
    success = await embedding_service.store_book_content_chunks(chunks)
    
    if success:
        print(f"Successfully stored {len(chunks)} chunks in Qdrant collection: {embedding_service.collection_name}")
    else:
        print("Failed to store chunks in Qdrant")
    
    return success


def main():
    # Check if directory argument is provided
    if len(sys.argv) != 2:
        print("Usage: python embed_content.py <content_directory>")
        print("Example: python embed_content.py ../docs")
        sys.exit(1)
    
    content_dir = sys.argv[1]
    
    # Verify the directory exists
    if not os.path.isdir(content_dir):
        print(f"Error: Directory does not exist: {content_dir}")
        sys.exit(1)
    
    print("Starting content embedding process...")
    print(f"Content directory: {content_dir}")
    
    # Run the embedding process
    success = asyncio.run(embed_book_content(content_dir))
    
    if success:
        print("Content embedding completed successfully!")
    else:
        print("Content embedding failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()