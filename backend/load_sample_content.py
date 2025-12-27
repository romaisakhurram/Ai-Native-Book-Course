"""
Simple script to load sample book content into the vector database
This script processes markdown files and stores their embeddings in Qdrant
"""
import asyncio
import sys
import os
from pathlib import Path

# Add the backend directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from services.embedding_service import EmbeddingService
from models.schemas import BookContentChunkCreate
from config.settings import settings
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def load_sample_content():
    """
    Load sample content into the vector database
    """
    logger.info("Starting sample content loading...")
    
    # Initialize the embedding service
    embedding_service = EmbeddingService()
    
    # Sample content - in a real scenario, this would come from actual book files
    sample_chapters = [
        {
            "id": "chapter_1_introduction",
            "title": "Chapter 1: Introduction to AI Native Applications",
            "content": """Introduction to AI Native Applications

Artificial Intelligence (AI) has rapidly evolved from a research concept to a practical technology that is transforming industries. AI Native applications are designed from the ground up to leverage AI capabilities as a core component of their architecture, rather than treating AI as an add-on feature.

Key characteristics of AI Native applications include:

1. Adaptive Behavior: The application learns and improves from interactions and data.
2. Context Awareness: The application understands and responds to environmental and user context.
3. Continuous Learning: The application updates its behavior based on new data without explicit programming.
4. Natural Interfaces: The application interacts with users through natural language, vision, or other modalities.

The architecture of AI Native applications typically involves:
- Data ingestion and preprocessing pipelines
- Model training and validation systems
- Real-time inference engines
- Feedback loops for continuous improvement

Traditional applications follow predetermined logic paths, while AI Native applications generate responses based on learned patterns and probabilistic models. This fundamental difference affects everything from development practices to deployment strategies and monitoring approaches."""
        },
        {
            "id": "chapter_2_foundations",
            "title": "Chapter 2: Foundations of Large Language Models",
            "content": """Foundations of Large Language Models

Large Language Models (LLMs) form the backbone of many AI Native applications. Understanding their architecture and capabilities is essential for building effective systems.

Transformer Architecture:
The transformer architecture, introduced in the paper 'Attention is All You Need,' revolutionized natural language processing. Key components include:

- Self-Attention Mechanisms: Allow the model to weigh the importance of different words in a sequence
- Positional Encoding: Helps the model understand the order of tokens in a sequence
- Feed-Forward Networks: Process each token independently after attention
- Multi-Head Attention: Enables the model to focus on different aspects of the input simultaneously

Training Process:
LLMs undergo multiple phases of training:
1. Pretraining: Learn general language patterns from large text corpora
2. Supervised Fine-Tuning: Adapt to specific tasks with labeled examples
3. Reinforcement Learning from Human Feedback (RLHF): Align model outputs with human preferences

Capabilities and Limitations:
LLMs demonstrate remarkable capabilities in:
- Text generation and completion
- Question answering
- Translation
- Summarization
- Code generation

However, they also have limitations including:
- Hallucinations (generating factually incorrect information)
- Limited reasoning capabilities for complex tasks
- High computational requirements
- Potential biases inherited from training data"""
        },
        {
            "id": "chapter_3_embeddings",
            "title": "Chapter 3: Embeddings and Vector Databases",
            "content": """Embeddings and Vector Databases

Embeddings are numerical representations of data that capture semantic meaning. In the context of text, embeddings represent words, phrases, or documents as vectors in a high-dimensional space.

What Are Embeddings?
An embedding is a dense vector representation of discrete data like text. Unlike sparse representations (like one-hot encodings), embeddings capture semantic relationships between data points. Words with similar meanings have similar embedding vectors.

Applications of Embeddings:
- Semantic search: Find documents similar in meaning to a query
- Clustering: Group related documents together
- Classification: Assign documents to categories based on content
- Recommendation: Suggest related content based on vector similarity

Vector Databases:
Vector databases are specialized databases designed to store and efficiently query high-dimensional vectors. They implement approximate nearest neighbor (ANN) algorithms to quickly find similar vectors.

Popular vector databases include:
- Qdrant: Open-source with rich filtering capabilities
- Pinecone: Managed service with automatic scaling
- Weaviate: GraphQL-powered with schema support
- Milvus: Open-source with enterprise features

Similarity Measures:
Different metrics measure similarity between vectors:
- Cosine similarity: Measures angle between vectors (most common for text embeddings)
- Euclidean distance: Measures straight-line distance between vectors
- Dot product: Measures the product of vector magnitudes and cosine of angle
"""
        },
        {
            "id": "chapter_4_rag",
            "title": "Chapter 4: Retrieval-Augmented Generation (RAG)",
            "content": """Retrieval-Augmented Generation (RAG)

Retrieval-Augmented Generation (RAG) combines the generative capabilities of LLMs with the precision of information retrieval. This approach enables applications to ground their responses in specific, authoritative sources.

Components of RAG Systems:
1. Indexer: Processes documents and stores them in a format suitable for retrieval
2. Retriever: Finds relevant documents based on user queries
3. Generator: Creates responses based on the query and retrieved context

RAG Pipeline:
The RAG process follows these steps:
1. Document Ingestion: Raw documents are parsed and preprocessed
2. Chunking: Documents are divided into smaller, semantically meaningful chunks
3. Embedding: Each chunk is converted to a vector representation
4. Storage: Embeddings and metadata are stored in a vector database
5. Query Processing: User queries are embedded and compared to stored vectors
6. Retrieval: Most similar chunks are retrieved based on vector similarity
7. Augmentation: Retrieved context is combined with the original query
8. Generation: LLM generates a response based on the augmented prompt

Benefits of RAG:
- Factuality: Responses are grounded in specific documents
- Freshness: Can incorporate recently added information
- Transparency: Sources for responses can be traced
- Accuracy: Reduces hallucinations by providing specific context
"""
        },
        {
            "id": "chapter_5_agents",
            "title": "Chapter 5: AI Agents and Tool Usage",
            "content": """AI Agents and Tool Usage

AI agents are systems that perceive their environment and take actions to achieve specific goals. Modern agents built with LLMs can plan, reason, and use tools to accomplish complex tasks.

Agent Components:
1. Planning: Breaks down complex tasks into manageable steps
2. Memory: Maintains state and context across interactions
3. Tool Usage: Interacts with external systems and APIs
4. Reflection: Evaluates and improves its own performance

Types of AI Agents:
- ReAct (Reason + Act): Combines reasoning and acting in a unified framework
- Chain-of-Thought: Uses intermediate reasoning steps to improve accuracy
- Toolformer: Leverages external tools like calculators and search engines
- Reflex Agents: Respond to stimuli based on predefined rules

Tool Usage:
Modern agents can use various tools including:
- Calculators for mathematical computations
- Search engines for information retrieval
- Databases for data lookup
- APIs for system integration
- Custom functions for domain-specific tasks

Best Practices for Agent Development:
- Clear goal specification
- Appropriate tool selection
- Error handling and recovery
- Monitoring and evaluation
- Safety and alignment considerations"""
        }
    ]
    
    # Convert sample chapters to content chunks
    chunks = []
    for chapter in sample_chapters:
        chunk = BookContentChunkCreate(
            chunk_id=chapter["id"],
            content=chapter["content"],
            document_id=chapter["title"],
            metadata={"chapter_title": chapter["title"]}
        )
        chunks.append(chunk)
    
    logger.info(f"Created {len(chunks)} content chunks for indexing")
    
    # Store the content chunks in the embedding service
    success = await embedding_service.store_book_content_chunks(chunks)
    
    if success:
        logger.info("Successfully stored sample content in the vector database")
        print("+ Sample content loaded successfully!")
        print(f"+ Loaded {len(chunks)} content chunks")
        print("+ Content is now available for semantic search")
    else:
        logger.error("Failed to store sample content in the vector database")
        print("X Failed to load sample content")
        
    return success

def main():
    print("Loading sample book content into the vector database...")
    print("This will allow the chatbot to answer questions based on actual content.")
    print("-" * 60)
    
    # Run the content loading
    success = asyncio.run(load_sample_content())
    
    if success:
        print("\n+ Content loading completed successfully!")
        print("The chatbot should now be able to answer questions based on the loaded content.")
    else:
        print("\nX Content loading failed!")
        print("The chatbot may not be able to provide meaningful responses.")

if __name__ == "__main__":
    main()