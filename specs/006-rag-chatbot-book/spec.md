# Feature Specification: Embedded RAG Chatbot for Markdown Book with Automated Setup

**Feature Branch**: `006-rag-chatbot-book`
**Created**: 2025-12-16
**Updated**: 2025-12-16
**Status**: Draft
**Input**: User description: "Update to include automated backend setup, dependency management, and enhanced integration capabilities"

## Clarifications

### Session 2025-12-16

- Q: What authentication model should be used for the chatbot? → A: No authentication required for basic chat functionality; sessions tied to browser/device only

## User Scenarios & Testing *(mandatory)*

<!--
  IMPORTANT: User stories should be PRIORITIZED as user journeys ordered by importance.
  Each user story/journey must be INDEPENDENTLY TESTABLE - meaning if you implement just ONE of them,
  you should still have a viable MVP (Minimum Viable Product) that delivers value.

  Assign priorities (P1, P2, P3, etc.) to each story, where P1 is the most critical.
  Think of each story as a standalone slice of functionality that can be:
  - Developed independently
  - Tested independently
  - Deployed independently
  - Demonstrated to users independently
-->

### User Story 1 - Ask Questions and Receive Answers from Book Content (Priority: P1)

As a book reader, I want to ask questions about the content I'm reading so that I can get answers based on the book's information without having to search through pages.

**Why this priority**: This is the core value proposition of the feature - enabling users to interact with the book in a conversational way for deeper understanding.

**Independent Test**: Can be fully tested by asking questions about a specific topic in the book and verifying that the chatbot returns accurate answers based on the book content.

**Acceptance Scenarios**:

1. **Given** I am reading a page in the book, **When** I ask a question related to the book's content, **Then** the chatbot provides an answer based on relevant sections from the book.
2. **Given** I have questions about concepts in the book, **When** I submit my question to the chatbot, **Then** I receive a response that references specific parts of the book content.

---

### User Story 2 - Ask Questions Based on Selected Text Only (Priority: P2)

As a book reader, I want to be able to highlight specific text in the book and ask questions that are answered only from that selected text, rather than the entire book.

**Why this priority**: This provides more control for users who want to focus their questions on specific parts of the content.

**Independent Test**: Can be tested by selecting text, asking a question related to that text, and verifying that the answer is limited to information from the selected text.

**Acceptance Scenarios**:

1. **Given** I have highlighted/selected text within the book, **When** I ask a question based on that selection, **Then** the chatbot provides an answer using only information from the selected text.
2. **Given** I am using the selected-text only mode, **When** I ask a question that relates to content outside my selection, **Then** the chatbot informs me that the answer is not available in the selected text.

---

### User Story 3 - Persist Chat Sessions and History (Priority: P3)

As a book reader, I want my chat sessions to be saved so that I can resume conversations with the chatbot later and review previous interactions.

**Why this priority**: This enhances the user experience by allowing for continuity in learning and information retrieval.

**Independent Test**: Can be tested by starting a conversation, leaving the book, and then returning to continue the conversation or view history.

**Acceptance Scenarios**:

1. **Given** I have asked several questions in a session, **When** I return to the book later, **Then** I can see my previous questions and answers.
2. **Given** I have multiple sessions with the chatbot, **When** I want to review past interactions, **Then** I can access and switch between different sessions.

---

### Edge Cases

- What happens when a user asks a question that doesn't have sufficient context in the book?
- How does the system handle very long queries or very large text selections?
- How does the system handle questions that require information from multiple unrelated sections of the book?
- What happens if the book content is updated while a chat session is in progress?
- How does the system handle network connectivity issues during a conversation?
- What happens when a user tries to access a session that has been purged due to retention policies?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide a chat interface embedded within the book website that allows users to ask questions about the book content
- **FR-002**: System MUST perform semantic search over the full book content to find relevant information when answering user questions
- **FR-003**: System MUST support a selected-text only mode where answers are generated exclusively from user-highlighted text
- **FR-004**: System MUST prevent hallucinations by enforcing that all answers are based solely on the book's content
- **FR-005**: System MUST persist chat sessions and metadata so users can resume conversations later
- **FR-006**: System MUST handle both full-book queries and selected-text queries with appropriate context boundaries
- **FR-007**: System MUST provide clear indicators when the chatbot is in selected-text only mode versus full-book mode
- **FR-008**: System MUST return answers that are traceable to specific sections or paragraphs in the book content
- **FR-009**: System MUST handle book content in Markdown format without requiring modifications to the original files
- **FR-010**: System MUST provide appropriate responses when questions cannot be answered from the available context
- **FR-011**: System MUST allow access to chat functionality without requiring user authentication, with sessions tied to browser/device only
- **FR-012**: System MUST automatically create a `backend` folder for the service implementation
- **FR-013**: System MUST initialize a Python project using `uv` package manager in the backend folder
- **FR-014**: System MUST install all required backend dependencies using `uv` including FastAPI, OpenRouter API client, Qdrant client, and Neon connector
- **FR-015**: System MUST implement a FastAPI backend service for RAG processing with endpoints for chat, session management, and semantic search
- **FR-016**: System MUST use OpenRouter API for LLM access to generate responses to user questions
- **FR-017**: System MUST use Qwen embeddings via OpenRouter for vectorizing book content and user queries
- **FR-018**: System MUST store document embeddings in Qdrant Cloud (Free Tier) for semantic search capabilities
- **FR-019**: System MUST store chat sessions and metadata in Neon Serverless Postgres database
- **FR-020**: System MUST embed the chatbot UI inside the book using OpenAI ChatKit SDK with seamless Docusaurus integration

*Example of marking unclear requirements:*

- **FR-021**: System MUST retain user sessions for 30 days unless the user explicitly deletes them

### Key Entities *(include if feature involves data)*

- **Chat Session**: Represents a conversation between a user and the chatbot, including metadata like creation time and user identifier
- **Query**: A question posed by the user, including context about whether it's for full-book or selected-text mode
- **Response**: An answer generated by the chatbot based on the book content, with references to source material
- **Book Content**: The Markdown-based content of the book that serves as the knowledge base for the chatbot
- **Selected Text**: A portion of text that the user has highlighted for the selected-text only mode
- **Embedding Vector**: Numerical representation of text content used for semantic similarity matching in Qdrant
- **Document Chunk**: Segments of the original book content that have been processed and stored with embeddings
- **Backend Service**: FastAPI application handling API requests, RAG processing, and database operations

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 85% of user questions receive relevant answers based on book content within 5 seconds of submission
- **SC-002**: Users can activate and use selected-text only mode successfully in 100% of attempts
- **SC-003**: Chat sessions are persisted and recoverable in 95% of cases when users return to the book
- **SC-004**: Less than 5% of responses contain information not found in the book (hallucinations)
- **SC-005**: The embedded chat interface loads within 3 seconds without degrading the book's core functionality
- **SC-006**: 80% of users who try the chatbot feature use it at least twice, indicating value retention
- **SC-007**: Users can accurately identify which parts of the book content were used to generate specific answers
- **SC-008**: Backend service can be set up automatically with `uv` in under 2 minutes
- **SC-009**: All required dependencies install correctly via `uv` without conflicts
- **SC-010**: Qdrant Cloud and Neon Postgres connections establish successfully during initialization
