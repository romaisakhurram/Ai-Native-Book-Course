# RAG Chatbot Agent - API Documentation

## Overview
The backend agent provides REST API endpoints for managing chat sessions and processing queries using the RAG (Retrieval Augmented Generation) pattern with Qwen LLM model.

---

## Base URL
```
http://localhost:8000/api/v1
```

## Authentication
Currently, no authentication is required. In production, implement JWT or API key authentication.

---

## Session Management Endpoints

### 1. Create Session
Creates a new chat session.

**Endpoint:** `POST /sessions`

**Request Body:**
```json
{
  "user_id": "user_123",
  "session_name": "My Book Discussion"
}
```

**Response (201):**
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "user_id": "user_123",
  "session_name": "My Book Discussion",
  "created_at": "2025-12-18T10:30:00Z",
  "last_activity": "2025-12-18T10:30:00Z"
}
```

**Error Responses:**
- `400`: Invalid request body
- `500`: Internal server error

---

### 2. Get Session
Retrieve details of an existing session.

**Endpoint:** `GET /sessions/{session_id}`

**Parameters:**
- `session_id` (string, path): Session UUID

**Response (200):**
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "user_id": "user_123",
  "session_name": "My Book Discussion",
  "created_at": "2025-12-18T10:30:00Z",
  "last_activity": "2025-12-18T10:35:00Z",
  "query_count": 5
}
```

**Error Responses:**
- `400`: Invalid session_id format
- `404`: Session not found
- `500`: Internal server error

---

### 3. Delete Session
End a chat session.

**Endpoint:** `DELETE /sessions/{session_id}`

**Parameters:**
- `session_id` (string, path): Session UUID

**Response (204):** No content (session deleted)

**Error Responses:**
- `400`: Invalid session_id format
- `404`: Session not found
- `500`: Internal server error

---

## Query Processing Endpoints

### 4. Submit Query
Submit a question to the chatbot within a session.

**Endpoint:** `POST /sessions/{session_id}/queries`

**Parameters:**
- `session_id` (string, path): Session UUID

**Request Body:**
```json
{
  "query_text": "What is ROS 2 and how does it work?",
  "query_mode": "FULL_BOOK",
  "selected_text": null
}
```

**Query Modes:**
- `FULL_BOOK`: Search across entire book content (default)
- `SELECTED_TEXT_ONLY`: Only use user-selected text

**Response (200):**
```json
{
  "query_id": "550e8400-e29b-41d4-a716-446655440001",
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "query_text": "What is ROS 2 and how does it work?",
  "response_text": "ROS 2 is a flexible middleware for writing robotic software. It provides a distributed framework with tools and libraries for building robot applications...",
  "source_chunks": [
    {
      "chunk_id": "chunk_001",
      "content": "ROS 2 (Robot Operating System 2) is a flexible middleware framework designed for robotics. It provides tools, libraries, and conventions for building robot applications...",
      "document_id": "module1/01-ros2-basics.md",
      "metadata": {
        "section": "Introduction",
        "page": 1
      }
    },
    {
      "chunk_id": "chunk_002",
      "content": "The DDS middleware in ROS 2 enables seamless communication between different nodes in a distributed system...",
      "document_id": "module1/02-ros2-communication.md",
      "metadata": {
        "section": "Communication",
        "page": 5
      }
    }
  ],
  "timestamp": "2025-12-18T10:35:00Z"
}
```

**Error Responses:**
- `400`: Invalid request format or invalid query mode
- `404`: Session not found
- `429`: Rate limit exceeded (100 req/hour)
- `500`: Internal server error

---

### 5. Get Query Response
Retrieve a previously asked question and its answer.

**Endpoint:** `GET /sessions/{session_id}/queries/{query_id}`

**Parameters:**
- `session_id` (string, path): Session UUID
- `query_id` (string, path): Query UUID

**Response (200):**
```json
{
  "query_id": "550e8400-e29b-41d4-a716-446655440001",
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "query_text": "What is ROS 2 and how does it work?",
  "response_text": "ROS 2 is a flexible middleware for writing robotic software...",
  "source_chunks": [...],
  "timestamp": "2025-12-18T10:35:00Z"
}
```

**Error Responses:**
- `400`: Invalid ID format
- `404`: Session or query not found
- `500`: Internal server error

---

## Health & Diagnostic Endpoints

### 6. Root Endpoint
Check if API is running.

**Endpoint:** `GET /`

**Response (200):**
```json
{
  "message": "RAG Chatbot API for Markdown Book",
  "version": "1.0.0"
}
```

---

### 7. Health Check
Health status of the API.

**Endpoint:** `GET /health`

**Response (200):**
```json
{
  "status": "healthy"
}
```

---

## Data Models

### SessionCreate
```
{
  "user_id": string          # Unique user identifier
  "session_name": string     # Human-readable session name
}
```

### QueryRequest
```
{
  "query_text": string       # User's question
  "query_mode": string       # "FULL_BOOK" or "SELECTED_TEXT_ONLY"
  "selected_text": string?   # Optional user-selected text
}
```

### SourceChunk
```
{
  "chunk_id": string         # Unique chunk identifier
  "content": string          # Chunk text content
  "document_id": string      # Source document path
  "metadata": object         # Additional metadata (section, page, etc.)
}
```

### QueryResponse
```
{
  "query_id": string         # Unique query identifier
  "session_id": string       # Session UUID
  "query_text": string       # Original query
  "response_text": string    # LLM response
  "source_chunks": array     # Retrieved context chunks
  "timestamp": string        # ISO 8601 timestamp
}
```

### TokenUsage
```
{
  "input_tokens": integer    # Tokens used in request
  "output_tokens": integer   # Tokens in response
}
```

---

## Error Response Format

All errors follow this format:

```json
{
  "detail": "Error message describing what went wrong"
}
```

### Common HTTP Status Codes

| Code | Meaning | Solution |
|------|---------|----------|
| 200 | OK | Request successful |
| 201 | Created | Resource created successfully |
| 204 | No Content | Operation successful (no body) |
| 400 | Bad Request | Invalid input, check request format |
| 404 | Not Found | Session or resource not found |
| 429 | Too Many Requests | Rate limit exceeded, wait before retrying |
| 500 | Server Error | Internal error, contact support |

---

## Rate Limiting

The API implements rate limiting:
- **Limit:** 100 requests per hour per IP address
- **Header:** `X-RateLimit-Limit: 100`
- **Remaining:** `X-RateLimit-Remaining: 95`
- **Reset Time:** `X-RateLimit-Reset: 1702891200`

When rate limit is exceeded, the API returns:
```
HTTP/1.1 429 Too Many Requests
```

---

## Caching

Query results are cached for 30 minutes. Identical queries within this period return cached responses for improved performance.

---

## Example Usage

### JavaScript/Fetch

```javascript
// 1. Create session
const sessionRes = await fetch('http://localhost:8000/api/v1/sessions', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    user_id: 'user_123',
    session_name: 'My Discussion'
  })
});
const session = await sessionRes.json();
const sessionId = session.session_id;

// 2. Submit query
const queryRes = await fetch(
  `http://localhost:8000/api/v1/sessions/${sessionId}/queries`,
  {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      query_text: 'What is ROS 2?',
      query_mode: 'FULL_BOOK',
      selected_text: null
    })
  }
);
const result = await queryRes.json();
console.log(result.response_text);
```

### Python

```python
import requests

BASE_URL = 'http://localhost:8000/api/v1'

# 1. Create session
session_data = {
    'user_id': 'user_123',
    'session_name': 'My Discussion'
}
session_res = requests.post(f'{BASE_URL}/sessions', json=session_data)
session_id = session_res.json()['session_id']

# 2. Submit query
query_data = {
    'query_text': 'What is ROS 2?',
    'query_mode': 'FULL_BOOK',
    'selected_text': None
}
query_res = requests.post(
    f'{BASE_URL}/sessions/{session_id}/queries',
    json=query_data
)
result = query_res.json()
print(result['response_text'])
```

### cURL

```bash
# 1. Create session
curl -X POST http://localhost:8000/api/v1/sessions \
  -H 'Content-Type: application/json' \
  -d '{
    "user_id": "user_123",
    "session_name": "My Discussion"
  }'

# Response contains session_id, then use it in next request

# 2. Submit query
SESSION_ID="550e8400-e29b-41d4-a716-446655440000"
curl -X POST http://localhost:8000/api/v1/sessions/$SESSION_ID/queries \
  -H 'Content-Type: application/json' \
  -d '{
    "query_text": "What is ROS 2?",
    "query_mode": "FULL_BOOK",
    "selected_text": null
  }'
```

---

## Testing

### Interactive API Documentation
Visit: `http://localhost:8000/docs`

This provides an interactive Swagger UI where you can test all endpoints directly in your browser.

### Automated Testing
Run the backend verification script:
```bash
python verify_backend.py
```

---

## Troubleshooting

### "Session not found"
- Ensure the session_id is a valid UUID
- Verify the session was created before querying
- Sessions may expire after inactivity (check implementation)

### "Invalid query mode"
- Use only "FULL_BOOK" or "SELECTED_TEXT_ONLY"
- Default is "FULL_BOOK"

### "Rate limit exceeded"
- Wait 1 hour for the limit to reset
- Implement exponential backoff in client
- Contact support for higher limits

### "No relevant context found"
- The query might not match any content in the database
- Try simpler or different keywords
- Ensure embeddings are uploaded to Qdrant

---

## Performance Notes

- **Average response time:** 1-3 seconds (varies with query complexity)
- **Max concurrent connections:** Limited by PostgreSQL pool
- **Vector search speed:** ~100ms per query (from Qdrant)
- **Caching:** Identical queries within 30 min window are instant

---

## Support

For issues or questions:
1. Check the error message detail
2. Review logs: `LOG_LEVEL=debug` in `.env`
3. Verify configuration in `.env`
4. Check Swagger UI at `/docs`

---

**API Version:** 1.0.0  
**Last Updated:** December 18, 2025  
**Status:** Production Ready
