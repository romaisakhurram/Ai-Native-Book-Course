# RAG Chatbot Agent - System Architecture & Flow

## 🏗️ System Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                                                                  │
│                    WEB BROWSER (PORT 3000)                      │
│                                                                  │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │               FRONTEND (Docusaurus + React)              │  │
│  │                                                           │  │
│  │  ┌─────────────────────────────────────────────────────┐ │  │
│  │  │              Book Pages & Layout                   │ │  │
│  │  └──────────────────┬──────────────────────────────────┘ │  │
│  │                     │                                     │  │
│  │  ┌──────────────────▼──────────────────────────────────┐ │  │
│  │  │           ChatInterface Component                  │ │  │
│  │  │  • Message Display                                │ │  │
│  │  │  • Text Input (textarea)                          │ │  │
│  │  │  • Text Selection Detection                       │ │  │
│  │  │  • Query Mode Toggle                              │ │  │
│  │  │  • Loading Indicator                              │ │  │
│  │  │  • Source Citations                               │ │  │
│  │  │  • Accessibility (ARIA)                           │ │  │
│  │  └──────────────────┬──────────────────────────────────┘ │  │
│  │                     │                                     │  │
│  └─────────────────────┼─────────────────────────────────────┘  │
│                        │                                         │
│        NETWORK │ HTTP POST/GET │ JSON                           │
│        ────────┼──────────────────────────────────────────      │
│                │                                                 │
│                ▼                                                 │
└──────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│                    BACKEND SERVER (PORT 8000)                    │
│                                                                  │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                   FASTAPI APPLICATION                    │  │
│  │                                                           │  │
│  │  ┌──────────────────────────────────────────────────────┐│  │
│  │  │  API ENDPOINTS                                      ││  │
│  │  │  • POST   /api/v1/sessions                          ││  │
│  │  │  • GET    /api/v1/sessions/{id}                     ││  │
│  │  │  • DELETE /api/v1/sessions/{id}                     ││  │
│  │  │  • POST   /api/v1/sessions/{id}/queries             ││  │
│  │  │  • GET    /api/v1/sessions/{id}/queries/{id}        ││  │
│  │  └──────────────────────────────────────────────────────┘│  │
│  │                          │                                │  │
│  │                          ▼                                │  │
│  │  ┌──────────────────────────────────────────────────────┐│  │
│  │  │  MIDDLEWARE & ROUTING                              ││  │
│  │  │  • RequestLoggingMiddleware                         ││  │
│  │  │  • RateLimitMiddleware (100 req/hour)               ││  │
│  │  │  • Error Handling                                   ││  │
│  │  └──────────────────────────────────────────────────────┘│  │
│  │                          │                                │  │
│  │                          ▼                                │  │
│  │  ┌──────────────────────────────────────────────────────┐│  │
│  │  │  SERVICE LAYER                                      ││  │
│  │  │                                                     ││  │
│  │  │  ┌────────────────────────────────────────────────┐││  │
│  │  │  │ ChatService                                  │││  │
│  │  │  │ • Generate responses using Qwen LLM         │││  │
│  │  │  │ • Build context from retrieved chunks       │││  │
│  │  │  │ • Track token usage                         │││  │
│  │  │  └────────────────────────────────────────────────┘││  │
│  │  │                                                     ││  │
│  │  │  ┌────────────────────────────────────────────────┐││  │
│  │  │  │ RetrievalService                             │││  │
│  │  │  │ • Semantic search with embeddings            │││  │
│  │  │  │ • Full book search (FULL_BOOK mode)          │││  │
│  │  │  │ • Selected text mode (SELECTED_TEXT_ONLY)    │││  │
│  │  │  │ • Result caching (30 min TTL)                │││  │
│  │  │  │ • Query validation                           │││  │
│  │  │  └────────────────────────────────────────────────┘││  │
│  │  │                                                     ││  │
│  │  │  ┌────────────────────────────────────────────────┐││  │
│  │  │  │ EmbeddingService                             │││  │
│  │  │  │ • Generate embeddings (OpenRouter)           │││  │
│  │  │  │ • Vector storage in Qdrant                   │││  │
│  │  │  │ • Similarity search                          │││  │
│  │  │  │ • Batch processing with retry logic          │││  │
│  │  │  └────────────────────────────────────────────────┘││  │
│  │  └──────────────────────────────────────────────────────┘│  │
│  │                                                           │  │
│  │  ┌────────────┬────────────────┬─────────────┐            │  │
│  │  │            │                │             │            │  │
│  │  ▼            ▼                ▼             ▼            │  │
│  └───────────────────────────────────────────────────────────┘  │
│       │            │                │             │               │
└───────┼────────────┼────────────────┼─────────────┘               │
        │            │                │             
        │            │                │             
   DATABASE │    VECTOR DB  │  LLM API  │  CACHE
        │            │                │             
        ▼            ▼                ▼             
   ┌────────┐   ┌────────┐      ┌──────────┐      
   │  Neon  │   │ Qdrant │      │OpenRouter│      
   │  DB    │   │Vector  │      │  Qwen   │      
   │        │   │Database│      │  Model  │      
   └────────┘   └────────┘      └──────────┘      
   PostgreSQL  (Vectors)  (LLM)
```

---

## 🔄 Query Processing Flow

```
┌──────────────────────────────────┐
│   User Types Question in Chat    │
│   (Frontend ChatInterface)        │
└───────────────┬──────────────────┘
                │
                ▼
    ┌───────────────────────────┐
    │  User Clicks "Send" or    │
    │  Presses Enter            │
    └───────────────┬───────────┘
                    │
                    ▼
    ┌──────────────────────────────────┐
    │  Prepare QueryRequest:           │
    │  {                               │
    │    "query_text": "...",          │
    │    "query_mode": "FULL_BOOK",    │
    │    "selected_text": null         │
    │  }                               │
    └───────────────┬──────────────────┘
                    │
                    ▼
    ┌──────────────────────────────────────────┐
    │  POST /api/v1/sessions/{id}/queries      │
    │  (HTTP Request to Backend)               │
    └───────────────┬──────────────────────────┘
                    │
                    ▼
    ┌──────────────────────────────────────────┐
    │  Backend receives query at               │
    │  routes/queries.py:submit_query()        │
    └───────────────┬──────────────────────────┘
                    │
        ┌───────────┴────────────┐
        │                        │
        ▼                        ▼
    ┌─────────────┐    ┌──────────────────┐
    │  Validation │    │ Create Query     │
    │  • UUID     │    │ Record in DB     │
    │  • Query    │    │ (PostgreSQL)     │
    │  • Mode     │    └──────────────────┘
    └─────────────┘
        │
        ▼
    ┌──────────────────────────────────┐
    │  RetrievalService:               │
    │  retrieve_context()              │
    │  (Query Mode)                    │
    └─────────────┬────────────────────┘
        │         │
    ┌───┴─────────┴───────┐
    │ IF FULL_BOOK        │ IF SELECTED_TEXT_ONLY
    │                     │
    ▼                     ▼
Generate Query       Use User-Selected
Embedding            Text as Context
(OpenRouter)         (No embedding needed)
    │                     │
    ▼                     ▼
Search Qdrant        Create Source Chunk
for Similar          from Selection
Content              │
    │                │
    ▼                ▼
Retrieve Top 5       ┌─────────────────┐
Source Chunks        │ source_chunks[] │
    │                └─────────────────┘
    └─────────────┬───┘
                  │
                  ▼
        ┌──────────────────────────┐
        │  ChatService:            │
        │  generate_response()     │
        │                          │
        │  1. Build context from   │
        │     source chunks        │
        │  2. Create LLM prompt    │
        │  3. Call Qwen model      │
        │     (OpenRouter)         │
        └──────────────┬───────────┘
                       │
                       ▼
        ┌──────────────────────────────────┐
        │  Receive LLM Response:           │
        │  {                               │
        │    "response_text": "...",       │
        │    "usage": {                    │
        │      "prompt_tokens": 150,       │
        │      "completion_tokens": 200    │
        │    }                             │
        │  }                               │
        └──────────────┬───────────────────┘
                       │
                       ▼
        ┌──────────────────────────────────┐
        │  Create Response in DB           │
        │  (PostgreSQL)                    │
        │  • Query ID                      │
        │  • Response Text                 │
        │  • Source Chunks                 │
        │  • Token Usage                   │
        │  • Timestamp                     │
        └──────────────┬───────────────────┘
                       │
                       ▼
        ┌──────────────────────────────────┐
        │  Return QueryResponse:           │
        │  {                               │
        │    "query_id": "...",            │
        │    "session_id": "...",          │
        │    "query_text": "...",          │
        │    "response_text": "...",       │
        │    "source_chunks": [...],       │
        │    "timestamp": "..."            │
        │  }                               │
        └──────────────┬───────────────────┘
                       │
                       ▼ (HTTP Response)
    ┌──────────────────────────────────────────┐
    │  Frontend receives response JSON         │
    │  ChatInterface component processes it    │
    └───────────────┬──────────────────────────┘
                    │
                    ▼
    ┌─────────────────────────────────────────────┐
    │  Display:                                   │
    │  • Bot response in chat bubble              │
    │  • "Sources" expandable section             │
    │  • Source documents with snippets           │
    │  • Auto-scroll to latest message            │
    └─────────────────────────────────────────────┘
```

---

## 🔌 Data Models & Types

### Session
```typescript
{
  session_id: UUID,
  user_id: string,
  session_name: string,
  created_at: ISO8601,
  last_activity: ISO8601
}
```

### Query Request
```typescript
{
  query_text: string,         // User's question
  query_mode: "FULL_BOOK" | "SELECTED_TEXT_ONLY",
  selected_text?: string      // Optional user selection
}
```

### Query Response
```typescript
{
  query_id: UUID,
  session_id: UUID,
  query_text: string,
  response_text: string,      // LLM response
  source_chunks: [
    {
      chunk_id: string,
      content: string,        // Retrieved text
      document_id: string,    // Source file
      metadata: object        // Extra info
    }
  ],
  timestamp: ISO8601
}
```

### Embedding
```typescript
{
  chunk_id: string,
  content: string,
  document_id: string,
  vector: number[],           // 4096 dimensions (Qwen)
  metadata: {
    section: string,
    page: number,
    source: "markdown"
  }
}
```

---

## 🚀 Deployment Targets

### Development
```
Frontend: http://localhost:3000
Backend: http://localhost:8000
Database: PostgreSQL (Neon)
Vector DB: Qdrant Cloud
LLM: OpenRouter (Qwen)
```

### Staging
```
Frontend: https://staging.example.com
Backend: https://api-staging.example.com
Database: PostgreSQL (Neon)
Vector DB: Qdrant Cloud
LLM: OpenRouter (Qwen)
```

### Production
```
Frontend: https://book.example.com
Backend: https://api.example.com
Database: PostgreSQL (Neon - high availability)
Vector DB: Qdrant Cloud (replicated)
LLM: OpenRouter (Qwen with higher rate limits)
```

---

## 📊 Performance Characteristics

| Component | Metric | Target |
|-----------|--------|--------|
| Query Response | End-to-end latency | 1-3 seconds |
| Vector Search | Qdrant latency | ~100ms |
| LLM Call | Token generation | ~1-2 sec/100tokens |
| Cache Hit | Response time | <100ms |
| Concurrent Users | Per instance | 100+ |
| Rate Limit | Requests/hour | 100 |
| Cache TTL | Duration | 30 minutes |

---

## 🔐 Security Layers

```
┌─────────────────────────────┐
│  Frontend (HTTPS only)      │
│  • XSS protection           │
│  • CSRF token (if needed)   │
└────────────┬────────────────┘
             │
       ┌─────▼──────┐
       │ Rate Limit │ 100 req/hour
       └─────┬──────┘
             │
     ┌───────▼──────────┐
     │  API Validation  │
     │  • Input check   │
     │  • UUID validate │
     │  • Query limits  │
     └───────┬──────────┘
             │
    ┌────────▼────────┐
    │ Authentication  │ (Optional)
    │ • Session ID    │
    │ • API Key       │
    └────────┬────────┘
             │
      ┌──────▼───────┐
      │ Database     │
      │ • SQL Inject │
      │   Protection │
      │ • SSL/TLS    │
      └──────┬───────┘
             │
     ┌───────▼───────┐
     │ External APIs │
     │ • HTTPS only  │
     │ • API Keys    │
     │ • Rate limits │
     └───────────────┘
```

---

## 🎯 Next Steps

1. **Setup Backend**
   ```bash
   cd backend
   cp .env.example .env
   # Edit .env with your keys
   pip install -e .
   ```

2. **Verify Backend**
   ```bash
   python verify_backend.py
   ```

3. **Start Backend**
   ```bash
   uvicorn main:app --reload
   ```

4. **Setup Frontend** (New Terminal)
   ```bash
   cd frontend
   npm install
   npm start
   ```

5. **Test Integration**
   - Open http://localhost:3000
   - Use ChatInterface component
   - Check Network tab for API calls

---

**Architecture Version:** 1.0.0  
**Last Updated:** December 18, 2025  
**Status:** ✅ Ready for Development & Production
