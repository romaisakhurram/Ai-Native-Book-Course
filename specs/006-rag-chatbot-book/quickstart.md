# Quickstart Guide: RAG Chatbot for Markdown Book

## Prerequisites

- Python 3.11+
- `uv` package manager
- Access to OpenRouter API (for Qwen embeddings and LLM)
- Qdrant Cloud account (free tier)
- Neon Serverless Postgres account

## Setup

### 1. Clone and Initialize the Project

```bash
# Create the backend directory
mkdir backend
cd backend

# Initialize a new Python project with uv
uv init
```

### 2. Install Dependencies

```bash
# Install required packages
uv add fastapi uvicorn python-dotenv openai qdrant-client psycopg2-binary sqlalchemy python-multipart
```

### 3. Environment Configuration

Create a `.env` file with your API keys and connection details:

```env
OPENROUTER_API_KEY=your_openrouter_api_key
QDRANT_URL=your_qdrant_cloud_url
QDRANT_API_KEY=your_qdrant_api_key
NEON_DATABASE_URL=postgresql://username:password@ep-xxxxxx.us-east-1.aws.neon.tech/dbname
```

### 4. Project Structure

```text
backend/
├── __init__.py
├── .env
├── .uv.toml or pyproject.toml
├── main.py
├── config/
│   └── settings.py
├── models/
│   ├── database.py
│   └── schemas.py
├── services/
│   ├── embedding_service.py
│   ├── retrieval_service.py
│   ├── chat_service.py
│   └── content_processor.py
├── api/
│   ├── deps.py
│   └── routes/
│       ├── sessions.py
│       └── queries.py
└── utils/
    ├── markdown_parser.py
    └── validators.py
```

## Running the Service

### 1. Start the Backend Service

```bash
# From the backend directory
uvicorn main:app --reload
```

### 2. Index Book Content

First, you'll need to process and index your Markdown book content:

```bash
# Process the book content and store in vector database
python -m scripts.index_book_content --source-path /path/to/markdown/files
```

### 3. Test the API

Create a new session:

```bash
curl -X POST http://localhost:8000/sessions \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test-user-123"}'
```

Submit a query:

```bash
curl -X POST http://localhost:8000/sessions/{session-id}/queries \
  -H "Content-Type: application/json" \
  -d '{
    "query_text": "What are the core components of ROS 2?",
    "query_mode": "FULL_BOOK"
  }'
```

## Frontend Integration

### 1. Embed ChatKit UI in Docusaurus

1. Install the ChatKit SDK in your Docusaurus project:
```bash
npm install @openai/chatkit
```

2. Add the chat interface to your Docusaurus pages:
```js
// In your Docusaurus component
import { ChatKit } from '@openai/chatkit';

function ChatInterface() {
  return (
    <div className="chat-container">
      <ChatKit 
        backendUrl="http://localhost:8000"
        sessionId="session-123"
      />
    </div>
  );
}
```

### 2. Text Selection Feature

Add text selection functionality to send selected text to the chat:

```js
// Add to your Docusaurus layout
function addTextSelectionHandler() {
  document.addEventListener('mouseup', function() {
    const selectedText = window.getSelection().toString().trim();
    if (selectedText) {
      // Send selected text to chat interface
      window.postMessage({
        type: 'TEXT_SELECTED',
        text: selectedText
      }, '*');
    }
  });
}
```

## Development Workflow

### Adding New Features

1. Update the data models in `models/schemas.py`
2. Implement the service logic in `services/`
3. Create the API endpoints in `api/routes/`
4. Write tests for new functionality
5. Update documentation as needed

### Running Tests

```bash
# Run all tests
python -m pytest

# Run tests with coverage
python -m pytest --cov=.
```

## Deployment

### Backend API

Deploy the FastAPI application to a cloud provider of your choice (AWS, GCP, Azure, Vercel, etc.) with the environment variables set.

### Frontend Integration

The Docusaurus book with embedded chat will be built and deployed as normal, with the chat interface connecting to the deployed backend API.

## Troubleshooting

### Common Issues

1. **Embedding API errors**: Ensure your OpenRouter API key is valid and you have access to the Qwen embedding model.
2. **Vector search returns no results**: Check that the book content has been properly indexed and embeddings generated.
3. **Database connection errors**: Verify your Neon Postgres connection string and credentials.

2. **Slow response times**: Consider optimizing your vector database queries or increasing the performance tier of your database provider.