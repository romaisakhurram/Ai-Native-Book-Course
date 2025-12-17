# Research Findings: Embedded RAG Chatbot UI for Book Website

## Overview
This document captures research findings for implementing a floating chatbot launcher, slide-in chat panel, text-selection interaction, streaming responses, and integration with the FastAPI backend for the Docusaurus-based book website.

## Decision: Architecture Pattern
**Rationale**: Implement using a React-based component approach that integrates with Docusaurus, using existing FastAPI backend services with possible extensions.

**Alternatives considered**:
- Custom vanilla JavaScript implementation: Rejected because it would require more code and maintenance than React components
- Third-party chat widget: Rejected because it wouldn't meet the requirement for seamless integration with the book content
- Standalone SPA approach: Rejected because it would require page reloads which violates the constraints

## Decision: Text Selection Context Integration
**Rationale**: Use the Selection API to capture selected text (limited to 500 words) and send it as context along with user questions to the backend. The selected text will be displayed in the chat interface to maintain context, but the highlight will be cleared from the main content.

**Alternatives considered**:
- Manual copy-paste: Rejected because it adds friction to the user experience
- Hidden selection capture: Rejected because users need to see what context they're providing
- Page-level context only: Rejected because the requirements specifically call for selected text functionality

## Decision: Session Storage for Chat History
**Rationale**: Use browser's sessionStorage to persist chat history within a user session. This ensures conversations persist when navigating between pages but don't carry over to new sessions (browser-based sessions only). This approach is simpler than server-side sessions while meeting requirements.

**Alternatives considered**:
- localStorage: Rejected because it persists across sessions which may be confusing for users
- Server-side storage: Rejected because it adds complexity and isn't needed for session-level persistence
- URL parameters: Rejected because it's not suitable for chat history storage

## Decision: Streaming Response Implementation
**Rationale**: Implement Server-Sent Events (SSE) to stream responses from the FastAPI backend to the UI for real-time display as tokens arrive. This meets the performance requirement of showing initial text within 1 second and provides a better UX than delayed responses.

**Alternatives considered**:
- Polling: Rejected because it's less efficient than streaming
- Chunked HTTP responses: Considered but SSE is more appropriate for chat applications
- Client-side generation: Rejected because responses come from RAG system on backend

## Decision: Responsive Design Approach
**Rationale**: Use CSS Flexbox/Grid with media queries to ensure the chat interface works on mobile and desktop devices. The slide-in panel will adapt its dimensions based on screen size and will be optimized for touch interactions on mobile devices.

**Alternatives considered**:
- Separate mobile app: Rejected because it's beyond scope
- Progressive Web App: Rejected because simple responsive design meets requirements
- Fixed positioning only: Rejected because it doesn't adapt to different screen sizes

## Decision: Backend API Integration
**Rationale**: Extend existing FastAPI backend endpoints to support the new UI requirements, particularly for handling selected text context and streaming responses. This leverages existing infrastructure and follows the OpenAI Agents/ChatKit SDK patterns with Qdrant as specified in the constitution.

**Alternatives considered**:
- New separate backend: Rejected because it adds unnecessary complexity
- Client-side processing: Rejected because RAG processing must happen on backend
- Third-party chat API: Rejected because it needs to integrate with specific book content

## Decision: Error Handling Strategy
**Rationale**: Implement message queuing for AI service unavailability. When the AI service is temporarily down, user messages will be temporarily stored locally and processed when the service becomes available again. This maintains user workflow during service interruptions.

**Alternatives considered**:
- Show error and disable chat: Rejected because it would interrupt user workflow
- Disable chat interface: Rejected because it reduces functionality
- Fallback to search: Rejected because it requires additional implementation and doesn't match the primary function of the feature