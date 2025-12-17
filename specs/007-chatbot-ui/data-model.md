# Data Model: Embedded RAG Chatbot UI

## Overview
This document defines the data structures and models for the embedded RAG chatbot UI, focusing on frontend state management and the data exchanged between the UI and backend services.

## Core Entities

### Chat Session
Represents a single user's interaction with the chatbot during a browser session, containing conversation history and context.

**Fields**:
- `sessionId`: string (auto-generated unique identifier)
- `createdAt`: timestamp (when the session started)
- `messages`: Message[] (ordered array of conversation messages)
- `isActive`: boolean (whether the session is currently active)

**Constraints**:
- Browser-based sessions: lost when browser is closed
- Session data stored in sessionStorage

### Message
Represents an individual message in the conversation history, either from the user or the AI.

**Fields**:
- `id`: string (auto-generated unique identifier)
- `type`: MessageType enum ('user' | 'ai')
- `content`: string (the text content of the message)
- `timestamp`: timestamp (when the message was created)
- `context`: MessageContext (optional context information like selected text)
- `status`: MessageStatus enum ('pending' | 'complete' | 'error' | 'queued')

**Validation Rules**:
- Content must be non-empty string
- Type must be one of the defined enum values
- Timestamp must be in ISO 8601 format
- Content length must not exceed system limits

### MessageContext
Information that provides context for a message, particularly selected text from the book.

**Fields**:
- `selectedText`: string | null (the text selected by the user, if any, max 500 words)
- `sourcePage`: string (the URL or identifier of the page where text was selected)
- `selectionMetadata`: object (additional properties about the selection)

**Validation Rules**:
- Selected text must be 500 words or less
- Selection must be cleared from main content when shown in chat context

### ChatRequest
The data structure sent from the UI to the backend when initiating a chat interaction.

**Fields**:
- `message`: string (the user's question or message)
- `context`: MessageContext (context information, including selected text)
- `sessionId`: string (the current session identifier)

**Validation Rules**:
- Message must be a non-empty string
- SessionId must be a valid session identifier
- Context can be null if no text is selected
- Selected text in context must not exceed 500 words

### ChatResponse
The data structure received from the backend containing the AI's response.

**Fields**:
- `responseId`: string (unique identifier for this response)
- `content`: string (the AI-generated response content)
- `timestamp`: timestamp (when the response was generated)
- `status`: 'success' | 'error' (the status of the response generation)
- `streamComplete`: boolean (indicates if streaming is complete, for SSE responses)

## State Management

### UI State Model
The frontend maintains several state properties to manage the chat interface:

- `isChatOpen`: boolean (whether the chat panel is currently open)
- `currentInput`: string (the user's current input in the chat textbox)
- `isLoading`: boolean (whether the app is waiting for a response)
- `error`: string | null (any current error message to display)
- `selectedText`: string | null (text currently selected in the book content)
- `queuedMessages`: ChatRequest[] (messages queued during AI service unavailability)

## API Data Flows

### New Message Flow
1. User types message and clicks send
2. UI captures current `selectedText` if any (max 500 words)
3. UI constructs `ChatRequest` object with message, context, and session ID
4. Request is sent to backend API via SSE for streaming
5. Backend processes request with RAG system using Qdrant
6. Backend streams response tokens in real-time to UI
7. UI displays tokens as they arrive and updates `messages` array

### Session Persistence
1. When user starts a new session, `sessionId` is generated
2. All messages are associated with this session
3. Session data is stored in `sessionStorage` (browser-based only)
4. When navigating to new pages, session data is retrieved from storage
5. When browser is closed, session data is lost

### Error Handling Flow
1. When AI service is unavailable, messages are queued in `queuedMessages`
2. UI indicates queuing status to user
3. When service becomes available, queued messages are processed
4. Messages are removed from queue after successful processing