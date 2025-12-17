# End-to-End Testing Guide

This document outlines how to test the end-to-end functionality between the frontend and backend API.

## Prerequisites

- Backend service running on http://localhost:8000 (or your configured URL)
- Frontend development server running
- Valid API keys in your .env file

## Test Scenarios

### 1. Session Creation and Management

1. Verify that creating a new session works:
   ```bash
   curl -X POST http://localhost:8000/api/v1/sessions \
        -H "Content-Type: application/json" \
        -d '{"user_id": "test-user"}'
   ```

2. Verify that retrieving an existing session works:
   ```bash
   curl -X GET http://localhost:8000/api/v1/sessions/{session-id}
   ```

### 2. Full Book Query Functionality

1. Submit a query with query_mode set to "FULL_BOOK":
   ```bash
   curl -X POST http://localhost:8000/api/v1/sessions/{session-id}/queries \
        -H "Content-Type: application/json" \
        -d '{
          "query_text": "What are the main concepts discussed in this book?",
          "query_mode": "FULL_BOOK"
        }'
   ```

2. Verify that a response is returned with source chunks from the book content.

### 3. Selected Text Query Functionality

1. Submit a query with query_mode set to "SELECTED_TEXT_ONLY":
   ```bash
   curl -X POST http://localhost:8000/api/v1/sessions/{session-id}/queries \
        -H "Content-Type: application/json" \
        -d '{
          "query_text": "What does this text explain?",
          "query_mode": "SELECTED_TEXT_ONLY",
          "selected_text": "Here is the specific text that the user selected."
        }'
   ```

2. Verify that the response is based only on the provided selected text.

### 4. Session History Retrieval

1. Create multiple queries in a session.
2. Retrieve the session history:
   ```bash
   curl -X GET http://localhost:8000/api/v1/sessions/{session-id}/history
   ```

3. Verify that all queries and responses are returned in chronological order.

### 5. Frontend Integration Testing

1. Load a Docusaurus page that includes the ChatInterface component
2. Verify that the chat interface loads correctly
3. Test the session creation
4. Test both "FULL_BOOK" and "SELECTED_TEXT_ONLY" modes
5. Verify that text selection is properly detected
6. Test sending and receiving messages
7. Verify that sources are displayed correctly

## Automated Testing

You can create automated tests using the Jest framework for the frontend and pytest for the backend:

### Backend API Tests
```bash
# Run backend tests
cd backend
python -m pytest tests/
```

### Frontend Component Tests
```bash
# Run frontend tests
cd frontend
npm test
```

## Health Checks

1. Verify the backend is healthy:
   ```bash
   curl -X GET http://localhost:8000/health
   ```

2. Verify the backend service is accessible from frontend:
   - Check browser network tab for API calls
   - Verify no CORS errors occur