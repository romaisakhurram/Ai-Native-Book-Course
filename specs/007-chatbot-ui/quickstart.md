# Quickstart Guide: Embedded RAG Chatbot UI

## Overview
This guide provides instructions for setting up and running the embedded RAG chatbot UI in the Docusaurus-based book website. The implementation follows OpenAI Agents/ChatKit SDK patterns with FastAPI, Neon, and Qdrant as specified in the project constitution.

## Prerequisites

- Node.js 18+ installed
- Yarn package manager installed
- Python 3.11+ installed
- Access to the Qdrant vector database
- Access to the FastAPI backend with RAG capabilities

## Getting Started

### 1. Clone and Setup the Repository

```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Install Docusaurus Dependencies

```bash
cd docusaurus-book
yarn install
```

### 3. Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the backend directory:

```bash
# Backend configuration
FASTAPI_PORT=8000
QDRANT_URL=http://localhost:6333
OPENAI_API_KEY=your_openai_api_key_here
```

### 5. Run the Local Development Server

```bash
# In the docusaurus-book directory
yarn start
```

This will start the Docusaurus development server on `http://localhost:3000`.

### 6. Run the Backend Server

```bash
# In the backend directory
uvicorn main:app --reload --port 8000
```

This will start the FastAPI server on `http://localhost:8000`.

### 7. Run Qdrant Vector Database

```bash
# Using Docker
docker run -p 6333:6333 -p 6334:6334 \
  -e QDRANT__SERVICE__API_KEY=your-api-key \
  qdrant/qdrant
```

## Adding the Chatbot UI to Your Docusaurus Site

### 1. Components Installation

The chatbot UI components are located in `src/components/Chatbot/`:

- `ChatLauncher.jsx`: The floating button that opens the chat panel
- `ChatPanel.jsx`: The slide-in chat panel container
- `ChatWindow.jsx`: The main chat interface with message history
- `Message.jsx`: Individual message component
- `SelectionHandler.js`: Handles text selection functionality

### 2. Integrate Components

Import and include the `ChatLauncher` component in your Docusaurus layout (typically in `src/pages/layout.js` or `docusaurus.config.js`):

```jsx
import ChatLauncher from '../components/Chatbot/ChatLauncher';

// Include <ChatLauncher /> in your layout JSX
```

### 3. Environmental Configuration

Add the following environment variables:

```bash
REACT_APP_CHAT_API_URL=http://localhost:8000/api/v1
REACT_APP_CHAT_WEBSOCKET_URL=ws://localhost:8000/ws
```

## Key Configuration Options

### Customizing the Chat Launcher
- Adjust position via CSS classes (default: bottom-right)
- Customize appearance with CSS variables
- Modify initial visibility settings

### Text Selection Settings
- Maximum text selection length: 500 words (enforced)
- Selection highlighting behavior: cleared from content but shown in chat context
- Context inclusion thresholds: configurable per page

### Session Management
- Session type: browser-based only (lost when browser closes)
- Session storage: sessionStorage
- Message queuing: enabled for AI service unavailability

### Streaming Configuration
- Response behavior: tokens displayed as they arrive
- Timeout settings: configurable
- Retry logic: automatic when service is available

## API Endpoints Used

The chat UI interacts with these backend endpoints:

- `POST /api/v1/chat/start` - Start a new chat session
- `POST /api/v1/chat/send` - Send a message and get response
- `POST /api/v1/chat/stream` - Send a message and stream response with queuing support

## Development Workflow

1. Make changes to UI components in `src/components/Chatbot/`
2. Test in the Docusaurus development server
3. Verify API interactions with the backend
4. Run tests to ensure functionality remains intact

## Running Tests

### Frontend Tests

```bash
cd docusaurus-book
yarn test
```

### Backend Tests

```bash
cd backend
pytest
```

## Troubleshooting

### Common Issues

1. **API Connection Errors**
   - Verify backend server is running
   - Check API URL configuration
   - Confirm CORS settings allow requests from frontend

2. **Text Selection Not Working**
   - Ensure SelectionHandler.js is properly integrated
   - Verify text selection event listeners are active
   - Check for CSS properties that might interfere with selection

3. **Session Data Not Persisting**
   - Confirm browser supports sessionStorage
   - Check for any browser extensions that might interfere
   - Verify session management logic

4. **Streaming Responses Not Working**
   - Verify Server-Sent Events are properly configured
   - Check backend streaming implementation
   - Confirm client-side event handling

5. **Message Queuing Issues**
   - Ensure the AI service unavailability detection is working
   - Verify queued messages are processed when service becomes available
   - Check for any message loss during queuing

## Performance Optimization

- Streaming responses should deliver initial text within 1 second
- UI responses should be under 100ms
- Page load times should be under 3 seconds with chatbot enabled
- Selected text context limited to 500 words to prevent overload