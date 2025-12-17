"""
Content processing service for parsing and chunking book content
"""
from typing import List, Dict, Any, Tuple
import re
from pathlib import Path
import logging
from ..models.schemas import BookContentChunkCreate

logger = logging.getLogger(__name__)

class ContentProcessor:
    def __init__(self, chunk_size: int = 1000, overlap: int = 100):
        """
        Initialize the content processor
        :param chunk_size: Maximum size of each content chunk in characters
        :param overlap: Number of characters to overlap between chunks
        """
        self.chunk_size = chunk_size
        self.overlap = overlap

    def load_markdown_content(self, file_path: str) -> str:
        """
        Load content from a markdown file
        :param file_path: Path to the markdown file
        :return: Content as a string
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            logger.info(f"Successfully loaded content from {file_path}")
            return content
        except Exception as e:
            logger.error(f"Error loading markdown content from {file_path}: {e}")
            raise

    def load_all_markdown_from_directory(self, directory_path: str) -> Dict[str, str]:
        """
        Load content from all markdown files in a directory
        :param directory_path: Path to the directory containing markdown files
        :return: Dictionary mapping file paths to content
        """
        content_dict = {}
        directory = Path(directory_path)
        
        for md_file in directory.rglob("*.md"):
            content = self.load_markdown_content(str(md_file))
            content_dict[str(md_file)] = content
            
        logger.info(f"Loaded content from {len(content_dict)} markdown files in {directory_path}")
        return content_dict

    def chunk_content(self, content: str, document_id: str) -> List[BookContentChunkCreate]:
        """
        Split content into chunks suitable for embedding
        :param content: The content to chunk
        :param document_id: Identifier for the source document
        :return: List of chunk objects ready for embedding
        """
        chunks = []
        
        # Split the content into sentences to avoid breaking them mid-sentence
        sentences = re.split(r'[.!?]+\s+', content)
        
        current_chunk = ""
        chunk_start = 0
        
        for i, sentence in enumerate(sentences):
            # Add the sentence to the current chunk
            if current_chunk:
                test_chunk = current_chunk + ". " + sentence
            else:
                test_chunk = sentence
            
            # Check if adding this sentence would exceed the chunk size
            if len(test_chunk) <= self.chunk_size:
                current_chunk = test_chunk
            else:
                # If the current chunk isn't empty, save it and start a new one
                if current_chunk:
                    chunk_obj = BookContentChunkCreate(
                        document_id=document_id,
                        content=current_chunk,
                        metadata={"start_position": chunk_start, "end_position": chunk_start + len(current_chunk)}
                    )
                    chunks.append(chunk_obj)
                    
                    # Start a new chunk with overlap
                    overlap_start = max(0, len(current_chunk) - self.overlap)
                    current_chunk = current_chunk[overlap_start:] + ". " + sentence
                    chunk_start = len(content) - len(current_chunk)  # Approximate position
                else:
                    # Sentence is longer than chunk_size, need to split it
                    sentence_chunks = self._split_long_sentence(sentence)
                    for chunk_text in sentence_chunks:
                        chunk_obj = BookContentChunkCreate(
                            document_id=document_id,
                            content=chunk_text,
                            metadata={"start_position": chunk_start, "end_position": chunk_start + len(chunk_text)}
                        )
                        chunks.append(chunk_obj)
                        chunk_start += len(chunk_text)
        
        # Add the last chunk if it's not empty
        if current_chunk.strip():
            chunk_obj = BookContentChunkCreate(
                document_id=document_id,
                content=current_chunk,
                metadata={"start_position": chunk_start, "end_position": chunk_start + len(current_chunk)}
            )
            chunks.append(chunk_obj)
        
        logger.info(f"Split content into {len(chunks)} chunks for document {document_id}")
        return chunks

    def _split_long_sentence(self, sentence: str) -> List[str]:
        """
        Split a sentence that is longer than the chunk size
        :param sentence: The long sentence to split
        :return: List of sentence pieces
        """
        if len(sentence) <= self.chunk_size:
            return [sentence]
        
        # Split by chunk_size, but try to break at reasonable boundaries
        chunks = []
        start = 0
        
        while start < len(sentence):
            end = min(start + self.chunk_size, len(sentence))
            
            # If we're not at the end, try to break at a space
            if end < len(sentence):
                # Look for the last space within the chunk
                space_index = sentence.rfind(' ', start, end)
                if space_index > start + self.chunk_size // 2:  # Only if the space is not too early
                    end = space_index
            
            chunks.append(sentence[start:end])
            start = end
            # Skip any leading spaces in the next chunk
            while start < len(sentence) and sentence[start] == ' ':
                start += 1
        
        return chunks

    def process_directory(self, directory_path: str) -> List[BookContentChunkCreate]:
        """
        Process an entire directory of markdown files, chunking each one
        :param directory_path: Path to the directory containing markdown files
        :return: List of all content chunks from all files
        """
        all_chunks = []
        
        # Load content from all markdown files
        content_dict = self.load_all_markdown_from_directory(directory_path)
        
        # Process each file's content
        for file_path, content in content_dict.items():
            chunks = self.chunk_content(content, file_path)
            all_chunks.extend(chunks)
        
        logger.info(f"Processed {len(content_dict)} files into {len(all_chunks)} total chunks")
        return all_chunks