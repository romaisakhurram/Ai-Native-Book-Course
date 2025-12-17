# Research: RAG Chatbot Implementation

## Decision: Technology Stack
- FastAPI for the backend API service
- Qdrant Cloud for vector storage and retrieval
- Neon Serverless Postgres for session and metadata storage
- OpenRouter API for LLM interactions
- Qwen embeddings for vectorizing book content
- Docusaurus integration with ChatKit UI

## Rationale
- FastAPI offers excellent performance and built-in async support for I/O-heavy operations typical in RAG systems
- Qdrant is well-suited for semantic search with efficient similarity matching
- Neon provides serverless PostgreSQL with easy scaling
- OpenRouter supports multiple LLM options with consistent API
- Qwen embeddings align with the project's requirements and are accessible via OpenRouter
- ChatKit UI provides a ready-made interface that can be embedded in Docusaurus

## Alternatives Considered
1. **Alternative Vector DBs**: 
   - Pinecone: More expensive, less free-tier friendly
   - Weaviate: More complex setup
   - Supabase Vector: Still in beta
   - Chose Qdrant for its free tier and Python client

2. **Alternative Backend Frameworks**:
   - Django: Too heavy for API-only service
   - Flask: Less performant than FastAPI for async operations
   - Express.js: Would require different language (Node.js)
   - Chose FastAPI for performance and Python consistency

3. **Alternative LLM Providers**:
   - OpenAI: Potentially more expensive
   - Anthropic: Good but requires separate integration
   - OpenRouter: Supports Qwen and multiple models with single API
   - Chose OpenRouter for Qwen access and flexibility

## Implementation Approach

### 1. Backend Service Architecture
- FastAPI application with async endpoints
- Services layer for embeddings, retrieval, and chat generation
- Repository layer for database operations
- Markdown processing pipeline for content indexing

### 2. Content Indexing Process
- Parse Markdown files from book source
- Chunk content into searchable segments
- Generate embeddings using Qwen model
- Store in Qdrant with metadata for retrieval

### 3. Query Processing
- User submits question via embedded UI
- In selected-text mode: use only provided text for context
- In full-book mode: perform semantic search in Qdrant
- Construct context from relevant content chunks
- Generate response using LLM while enforcing book-only content
- Return response with source references

### 4. Session Management
- Store conversation history in Neon Postgres
- Track user selections and query context
- Maintain session state across page views

## Security Considerations
- Input validation for user queries
- Rate limiting to prevent abuse
- Secure API key management
- Proper session handling

## Performance Optimizations
- Caching for frequently accessed content
- Efficient vector search with Qdrant
- Asynchronous processing where appropriate
- Connection pooling for database operations