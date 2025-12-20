import os
import logging
from typing import List, Dict, Any
from pathlib import Path
import markdown
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, ServiceContext
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core.node_parser import SentenceSplitter

logger = logging.getLogger(__name__)

class BookContentService:
    """
    Service to handle book content processing, indexing, and response generation
    """
    
    def __init__(self):
        self.index = None
        self.documents = []
        self.setup_llm()
        self.load_and_index_content()
    
    def setup_llm(self):
        """
        Setup the LLM for response generation
        """
        # Using OpenAI by default, but can be configured differently
        self.llm = OpenAI(model="gpt-3.5-turbo")
        self.embedding_model = OpenAIEmbedding()
        
        # Create service context with LLM and embedding model
        self.service_context = ServiceContext.from_defaults(
            llm=self.llm,
            embed_model=self.embedding_model
        )
    
    def load_and_index_content(self):
        """
        Load book content from docs and book directories and create an index
        """
        try:
            # Define content directories to search
            content_dirs = [
                "docs",
                "book",
                "frontend/docs",
                "frontend/blog"
            ]
            
            # Find directories that exist
            existing_dirs = []
            for directory in content_dirs:
                full_path = Path(directory)
                if full_path.exists():
                    existing_dirs.append(str(full_path))
            
            if not existing_dirs:
                logger.warning("No content directories found. Using sample content.")
                # Create sample content if no directories exist
                self.create_sample_content()
                existing_dirs = ["sample_content"]
            
            # Load documents from all content directories
            documents = SimpleDirectoryReader(
                input_dir=",".join(existing_dirs),
                recursive=True,
                required_exts=[".md", ".mdx", ".txt"]
            ).load_data()
            
            # Parse documents into nodes
            node_parser = SentenceSplitter(chunk_size=512, chunk_overlap=50)
            nodes = node_parser.get_nodes_from_documents(documents)
            
            # Create index from nodes
            self.index = VectorStoreIndex(nodes, service_context=self.service_context)
            logger.info(f"Successfully indexed {len(nodes)} content chunks")
            
        except Exception as e:
            logger.error(f"Error loading and indexing content: {str(e)}")
            raise
    
    def create_sample_content(self):
        """
        Create sample content if no content directories exist
        """
        os.makedirs("sample_content", exist_ok=True)
        with open("sample_content/sample.md", "w") as f:
            f.write("# Sample Book Content\n\nThis is sample content for the AI agent to demonstrate functionality.\n\n## Chapter 1\n\nContent for chapter 1 goes here.\n\n## Chapter 2\n\nContent for chapter 2 goes here.")
    
    def generate_response(self, query: str, context: str = None) -> str:
        """
        Generate a response to the user's query using the indexed content
        """
        try:
            if self.index is None:
                raise Exception("Content index not initialized")
            
            # Create a query engine
            query_engine = self.index.as_query_engine(
                similarity_top_k=5,
                response_mode="compact"
            )
            
            # Query the index
            response = query_engine.query(query)
            
            # Return the response text
            return str(response)
        
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return f"I encountered an error processing your request: {str(e)}"
    
    def search_content(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Search for content relevant to the query
        """
        try:
            if self.index is None:
                raise Exception("Content index not initialized")
            
            # Create a retriever
            retriever = self.index.as_retriever(similarity_top_k=limit)
            
            # Retrieve relevant nodes
            nodes = retriever.retrieve(query)
            
            # Convert nodes to dictionary format
            results = []
            for node in nodes:
                results.append({
                    "id": node.node_id,
                    "score": node.score,
                    "content": node.text,
                    "metadata": node.metadata
                })
            
            return results
        
        except Exception as e:
            logger.error(f"Error searching content: {str(e)}")
            return []