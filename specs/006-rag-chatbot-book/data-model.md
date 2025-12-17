# Data Model: RAG Chatbot for Markdown Book

## Core Entities

### Chat Session
- **session_id**: UUID, Primary Key
- **user_id**: UUID (optional, for logged-in users)
- **created_at**: DateTime
- **updated_at**: DateTime
- **metadata**: JSON (for additional context)
- **is_active**: Boolean

### Query
- **query_id**: UUID, Primary Key
- **session_id**: UUID, Foreign Key to Chat Session
- **query_text**: Text
- **query_mode**: Enum (FULL_BOOK, SELECTED_TEXT_ONLY)
- **selected_text**: Text (optional, for selected-text mode)
- **timestamp**: DateTime
- **source_reference**: Text (optional, page/chapter reference)

### Response
- **response_id**: UUID, Primary Key
- **query_id**: UUID, Foreign Key to Query
- **response_text**: Text
- **timestamp**: DateTime
- **source_chunks**: JSON (references to book content used)
- **token_usage**: JSON (LLM token usage metrics)

### Book Content Chunk
- **chunk_id**: UUID, Primary Key
- **document_id**: Text (identifier for the source document)
- **content**: Text (the actual content chunk)
- **metadata**: JSON (source location, headings, etc.)
- **embedding**: Vector (Qwen embedding)
- **hash**: Text (for change detection)

### User Selection
- **selection_id**: UUID, Primary Key
- **session_id**: UUID, Foreign Key to Chat Session
- **content**: Text (the selected text)
- **source_location**: Text (where in the book this text appears)
- **created_at**: DateTime
- **query_id**: UUID (optional, Foreign Key to Query if used in a question)

## Relationships

- Chat Session (1) → (Many) Query
- Query (1) → (1) Response
- Query (1) → (0 or Many) User Selection
- Book Content Chunk (Many) → (Many) Response (via source_chunks reference)

## Validation Rules

### Chat Session
- session_id must be unique
- created_at must be set on creation
- updated_at must be updated on changes

### Query
- session_id must reference an existing Chat Session
- query_mode must be either 'FULL_BOOK' or 'SELECTED_TEXT_ONLY'
- if query_mode is 'SELECTED_TEXT_ONLY', selected_text must not be empty

### Response
- query_id must reference an existing Query
- response_text must not be empty
- token_usage must follow the format {input_tokens: integer, output_tokens: integer}

### Book Content Chunk
- document_id must identify the source document uniquely
- embedding must be a valid vector
- hash must be computed from content for change detection

### User Selection
- session_id must reference an existing Chat Session
- content must not be empty
- created_at must be set on creation

## State Transitions

### Chat Session
- ACTIVE (when created or when receiving new queries)
- INACTIVE (after period of inactivity or explicit closure)

## Indexes

- Chat Session: index on user_id and updated_at for session retrieval
- Query: index on session_id and timestamp for chronological query access
- Book Content Chunk: index on document_id for efficient document-based retrieval
- Book Content Chunk: vector index on embedding for semantic search