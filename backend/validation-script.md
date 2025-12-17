# Quickstart Validation Script

This script validates that the RAG Chatbot setup is working correctly based on the quickstart guide.

## Prerequisites Validation

1. Verify Python 3.11+:
   ```bash
   python --version
   # Should be Python 3.11 or higher
   ```

2. Verify `uv` package manager:
   ```bash
   uv --version
   # Should return version information
   ```

3. Check that required API keys are in place:
   - OPENROUTER_API_KEY
   - QDRANT_URL
   - QDRANT_API_KEY
   - NEON_DATABASE_URL

## Backend Service Validation

1. Start the backend service:
   ```bash
   # From the backend directory
   cd backend
   uvicorn main:app --reload
   ```

2. Verify the service is running:
   ```bash
   curl http://localhost:8000/health
   # Should return: {"status": "healthy"}
   ```

3. Create a test session:
   ```bash
   curl -X POST http://localhost:8000/api/v1/sessions \
        -H "Content-Type": "application/json" \
        -d '{"user_id": "test-user"}'
   # Should return session information with a new session_id
   ```

4. Submit a test query:
   ```bash
   curl -X POST http://localhost:8000/api/v1/sessions/{SESSION_ID}/queries \
        -H "Content-Type": "application/json" \
        -d '{
          "query_text": "Test query",
          "query_mode": "FULL_BOOK"
        }'
   # Should return a query response with the bot's answer
   ```

## Frontend Integration Validation

1. Install dependencies in frontend:
   ```bash
   cd frontend
   npm install
   ```

2. Run the Docusaurus development server:
   ```bash
   npm run start
   ```

3. Verify the ChatInterface component loads properly on a page.

## Content Indexing Validation

1. Process the book content:
   ```bash
   python -m scripts.index_book_content --source-path /path/to/markdown/files
   # Should process files and store in vector database
   ```

## Final Validation

Once all steps pass, the RAG Chatbot implementation is correctly set up and functional.