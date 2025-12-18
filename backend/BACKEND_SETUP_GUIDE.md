# Backend Setup Guide - RAG Chatbot Agent

## Status: ✅ Architecture Complete

The backend is fully architected with all required services and routes for the RAG chatbot agent. Below is the complete setup and deployment guide.

---

## 1. Backend Architecture Overview

### Core Services
- **ChatService** (`services/chat_service.py`): Generates AI responses using OpenRouter/Qwen model
- **RetrievalService** (`services/retrieval_service.py`): Performs semantic search on book content
- **EmbeddingService** (`services/embedding_service.py`): Manages vector embeddings with Qdrant
- **API Routes**: Sessions (`routes/sessions.py`) and Queries (`routes/queries.py`)

### Main Components
```
backend/
├── main.py                           # FastAPI app entry point
├── config/settings.py                # Environment configuration
├── api/routes/
│   ├── sessions.py                  # Session management endpoints
│   └── queries.py                   # Query processing endpoints
├── services/
│   ├── chat_service.py              # LLM response generation
│   ├── retrieval_service.py         # Semantic search & context retrieval
│   └── embedding_service.py         # Vector embeddings with Qdrant
├── models/
│   ├── schemas.py                   # Pydantic models (QueryRequest, QueryResponse, etc.)
│   ├── database.py                  # SQLAlchemy ORM models
│   └── chat_models.py               # Chat-related models
├── middleware/
│   ├── request_logging.py           # Request/response logging
│   └── rate_limit.py                # Rate limiting (100 req/hour)
└── utils/
    ├── db_operations.py             # Database CRUD operations
    ├── caching.py                   # Response caching (30 min)
    └── logging_config.py            # Logging configuration
```

---

## 2. Environment Setup

### Create `.env` file in `backend/` directory:

```env
# OpenRouter API (for Qwen model)
OPENROUTER_API_KEY=your_openrouter_api_key_here

# Qdrant Vector Database
QDRANT_URL=https://your-qdrant-instance.com
QDRANT_API_KEY=your_qdrant_api_key
QDRANT_BASE_URL=https://localhost:6333
QDRANT_COLLECTION_NAME=Ai-book

# Neon Database (PostgreSQL)
NEON_DATABASE_URL=postgresql://user:password@host/dbname

# Optional: OpenAI (fallback, not used if OpenRouter key is set)
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=qwen/qwen3-embedding-8b

# Logging
LOG_LEVEL=info
```

**Required Keys:**
- `OPENROUTER_API_KEY` ✅ Required
- `QDRANT_URL` ✅ Required  
- `QDRANT_API_KEY` ✅ Required
- `NEON_DATABASE_URL` ✅ Required

---

## 3. Installation & Prerequisites

### Python Version
- **Required:** Python 3.13+
- **Check:** `python --version`

### Install Dependencies

```bash
# Navigate to backend directory
cd backend

# Install dependencies (using pip or uv)
pip install -e .
# or with uv:
uv pip install -e .
```

### Key Dependencies
- **FastAPI** 0.124.4+ - Web framework
- **Uvicorn** 0.38.0+ - ASGI server
- **Qdrant-Client** 1.16.2+ - Vector database client
- **OpenAI** 2.12.0+ - LLM API client
- **SQLAlchemy** 2.0.45+ - ORM
- **Pydantic-Settings** 2.12.0+ - Configuration management
- **aioredis** 2.0.1+ - Async caching
- **psycopg2-binary** 2.9.11+ - PostgreSQL driver

---

## 4. Starting the Backend Server

### Option 1: Direct Run (Development)
```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Option 2: Production Run (No reload)
```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Verify Server is Running
- API Root: `http://localhost:8000/`
- Health Check: `http://localhost:8000/health`
- API Docs: `http://localhost:8000/docs` (Swagger UI)

---

## 5. API Endpoints

### Sessions Management
```
POST   /api/v1/sessions              - Create a new chat session
GET    /api/v1/sessions/{id}         - Get session details
DELETE /api/v1/sessions/{id}         - End a session
```

### Query Processing
```
POST   /api/v1/sessions/{session_id}/queries          - Submit query
GET    /api/v1/sessions/{session_id}/queries/{query_id} - Retrieve query response
```

### Example Query Request
```json
{
  "query_text": "What is ROS 2?",
  "query_mode": "FULL_BOOK",
  "selected_text": null
}
```

### Query Modes
- **FULL_BOOK** - Search across all embedded content
- **SELECTED_TEXT_ONLY** - Only use the user-selected text

---

## 6. Database Setup

### PostgreSQL (Neon)
The backend uses Neon Database (PostgreSQL) via SQLAlchemy ORM. Tables are automatically created on startup:

- `chat_sessions` - Stores user sessions
- `queries` - Stores user queries
- `responses` - Stores LLM responses
- `book_content_chunks` - Stores book content chunks (for reference)

**Auto-creation:** On startup, `Base.metadata.create_all(bind=engine)` creates all tables if they don't exist.

---

## 7. Vector Database (Qdrant) Setup

### Collection: `Ai-book`
- **Vector Size:** 4096 (Qwen3-embedding-8b model)
- **Distance Metric:** Cosine similarity
- **Auto-created:** On first embed operation or explicit creation

### Upload Content to Qdrant
Use the embedding scripts from the root directory:

```bash
# From root directory
python run_embedding_process.py
# or
python embed_content.py
```

These scripts:
1. Read markdown files from `frontend/docs/`
2. Generate embeddings using OpenRouter
3. Store vectors in Qdrant collection `Ai-book`

---

## 8. Query Flow (Agent Workflow)

```
User Query (Frontend)
        ↓
    FastAPI Route (/api/v1/sessions/{id}/queries)
        ↓
    Validation (QueryRequest schema)
        ↓
    RetrievalService.retrieve_context()
        ├─→ EmbeddingService: Generate query embedding
        └─→ Qdrant: Semantic search (retrieve top 5 chunks)
        ↓
    ChatService.generate_response()
        ├─→ Build context from retrieved chunks
        ├─→ Call OpenRouter Qwen model
        └─→ Return response + sources
        ↓
    Save to PostgreSQL (Query + Response)
        ↓
    Return QueryResponse to Frontend
        ↓
    Display in ChatInterface component
```

---

## 9. Middleware & Features

### Rate Limiting
- **Limit:** 100 requests per hour per IP
- **Middleware:** `RateLimitMiddleware`

### Request Logging
- **Logs:** Request method, path, status, response time
- **Middleware:** `RequestLoggingMiddleware`

### Caching
- **Duration:** 30 minutes
- **Service:** RetrievalService caches query results
- **Backend:** aioredis (async Redis)

---

## 10. Error Handling

### HTTP Status Codes
- `200` - Success
- `400` - Invalid query or validation error
- `404` - Session/Query not found
- `429` - Rate limit exceeded
- `500` - Internal server error

### Error Response Format
```json
{
  "detail": "Error message describing what went wrong"
}
```

---

## 11. Debugging & Logs

### Enable SQL Logging
Edit `backend/config/settings.py`:
```python
db_echo: bool = True  # Set to True to log SQL queries
```

### Log Levels
Set `LOG_LEVEL` in `.env`:
- `debug` - Verbose logging
- `info` - Standard logging (default)
- `warning` - Only warnings and errors
- `error` - Only errors

### View Logs
```bash
# Logs appear in console output when running with uvicorn
# Also check application logs directory if configured
```

---

## 12. Frontend Integration

### Backend URL Configuration
The frontend fetches from the backend using:

**Order of precedence:**
1. `REACT_APP_BACKEND_URL` environment variable
2. `backendUrl` prop passed to ChatInterface
3. `window.__BACKEND_URL__` global variable
4. Default: `http://localhost:8000`

### Set Frontend Backend URL
```bash
# In frontend/.env or frontend/.env.local
REACT_APP_BACKEND_URL=http://localhost:8000
# or for production
REACT_APP_BACKEND_URL=https://your-api.com
```

### CORS Configuration (if needed)
Add to `backend/main.py`:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 13. Deployment Checklist

- [ ] `.env` file created with all required keys
- [ ] Python 3.13+ installed
- [ ] Dependencies installed: `pip install -e .`
- [ ] Qdrant instance accessible and collection created
- [ ] PostgreSQL (Neon) database accessible
- [ ] OpenRouter API key validated
- [ ] `uvicorn main:app` starts without errors
- [ ] Health check endpoint responds: `GET /health` → `{"status": "healthy"}`
- [ ] API docs available: `GET /docs`
- [ ] Create test session: `POST /api/v1/sessions`
- [ ] Submit test query: `POST /api/v1/sessions/{id}/queries`
- [ ] Frontend can connect to backend (check browser console for CORS)

---

## 14. Production Considerations

### Security
- ✅ Use HTTPS for all external APIs
- ✅ Rotate API keys regularly
- ✅ Validate all user inputs
- ✅ Implement authentication for session endpoints
- ✅ Use rate limiting (already implemented)

### Performance
- ✅ Caching enabled (30 min TTL)
- ✅ Batch embeddings (5 chunks per request)
- ✅ Connection pooling configured
- ✅ Async/await for all I/O operations

### Monitoring
- Add application monitoring (e.g., Sentry, New Relic)
- Monitor Qdrant collection size and search latency
- Track API response times and error rates
- Monitor PostgreSQL connection pool usage

### Scaling
- Use multiple Uvicorn workers: `--workers 4` (or more)
- Configure Redis for distributed caching
- Use PostgreSQL read replicas for read-heavy workloads
- Monitor Qdrant instance for scaling needs

---

## 15. Troubleshooting

### Issue: "OPENROUTER_API_KEY not found"
**Solution:** Add key to `.env` and restart server

### Issue: "Qdrant connection refused"
**Solution:** Verify `QDRANT_URL` is correct and Qdrant instance is running

### Issue: "No module named 'backend'"
**Solution:** Run `pip install -e .` from backend directory

### Issue: "UUID validation error"
**Solution:** Ensure session_id and query_id are valid UUIDs

### Issue: "Collection does not exist"
**Solution:** Run embedding script to create collection and populate vectors

### Issue: CORS errors in frontend
**Solution:** Add CORSMiddleware to `main.py` with correct allowed origins

---

## 16. Next Steps

1. **Set up environment:** Create `.env` with required keys
2. **Install dependencies:** `pip install -e .`
3. **Start server:** `uvicorn main:app --reload`
4. **Verify:** Check `/health` endpoint
5. **Create content:** Run embedding script to populate Qdrant
6. **Test API:** Use Swagger UI at `/docs`
7. **Connect frontend:** Update `REACT_APP_BACKEND_URL`
8. **Deploy:** Follow production checklist

---

## Support & Resources

- **FastAPI Docs:** https://fastapi.tiangolo.com/
- **Qdrant Docs:** https://qdrant.tech/documentation/
- **OpenRouter Docs:** https://openrouter.ai/docs
- **SQLAlchemy Docs:** https://docs.sqlalchemy.org/

---

**Last Updated:** December 18, 2025
**Backend Version:** 1.0.0
**Status:** Ready for Development & Production Deployment
