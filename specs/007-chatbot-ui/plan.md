# Implementation Plan: Embedded RAG Chatbot UI for Book Website

**Branch**: `007-chatbot-ui` | **Date**: 2025-12-17 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/007-chatbot-ui/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

The embedded RAG chatbot UI implementation requires creating a floating chat launcher and slide-in chat panel that integrates with a Docusaurus-based book website. The UI must support text selection interaction to provide contextual Q&A about book content, connecting to a FastAPI backend for RAG processing. The implementation will ensure session persistence and smooth user experience across page navigations, adhering to minimal and professional design principles that don't intrude on the reading flow. Implementation will follow OpenAI Agents/ChatKit SDK patterns with FastAPI, Neon, and Qdrant as specified in the project constitution.

## Technical Context

**Language/Version**: JavaScript/TypeScript for frontend UI components, Python 3.11 for backend services
**Primary Dependencies**: React for chat interface components, FastAPI for backend API, Docusaurus for book website integration, Qdrant for vector storage
**Storage**: Browser session storage for chat history persistence (N/A for server storage), Qdrant for RAG vector storage
**Testing**: Jest for frontend components, pytest for backend API
**Target Platform**: Web browser (Chrome, Firefox, Safari, Edge) - both desktop and mobile
**Project Type**: Web application (frontend components integrated with Docusaurus book website)
**Performance Goals**: UI responses under 100ms, streaming responses display first token within 1 second, page load time under 3 seconds with chatbot enabled
**Constraints**: Must integrate seamlessly with Docusaurus Markdown-based website, no page reloads during interactions, responsive design for mobile and desktop, 500-word limit for selected text context
**Scale/Scope**: Single-page application overlay for book content, supporting text selection and contextual chat with real-time streaming

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Based on the Physical AI & Humanoid Robotics Constitution:

- **I. Technical Accuracy**: The implementation will ensure accurate integration with the RAG system using Qdrant for vector storage and proper handling of contextual questions. All UI components will function correctly with the Docusaurus framework and maintain technical accuracy for RAG systems.

- **II. Clear Explanations**: The UI will provide clear affordances for users to understand how to interact with the chatbot, ask questions about selected text (with 500-word limit), and navigate the conversation history.

- **III. Reproducibility**: The implementation will include clear documentation on how to integrate the chatbot UI with the Docusaurus book website, ensuring others can reproduce the setup. All code examples will be runnable.

- **IV. Consistent Structure**: The implementation will follow established patterns in the codebase, aligning with other UI components in the book website and maintaining consistent structure across the project.

**Chatbot Pattern Compliance**: The chatbot will follow the OpenAI Agents/ChatKit SDK patterns with FastAPI, Neon, and Qdrant as specified in the constitution.

**Constraints Compliance**: The implementation will ensure the chatbot responses rely only on book content or selected text as specified in the constitution, with responses streaming in real-time as tokens arrive.

## Project Structure

### Documentation (this feature)

```text
specs/007-chatbot-ui/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
# Web application structure (frontend components integrated with Docusaurus)
docusaurus-book/
├── src/
│   ├── components/
│   │   └── Chatbot/
│   │       ├── ChatLauncher.jsx      # Floating chat launcher
│   │       ├── ChatPanel.jsx         # Slide-in chat panel
│   │       ├── ChatWindow.jsx        # Main chat interface
│   │       ├── Message.jsx           # Individual message component
│   │       └── SelectionHandler.js   # Text selection integration
│   ├── pages/
│   └── utils/
│       └── session-storage.js        # Chat history persistence
├── static/
└── docusaurus.config.js              # Integration configuration
```

### Backend API (existing infrastructure)
```text
backend/
├── api/
│   └── v1/
│       └── endpoints/
│           ├── chat.py               # Chat endpoints
│           └── rag.py                # RAG processing endpoints
├── core/
│   └── rag_service.py                # RAG service implementation
└── models/
    └── chat_models.py                # Request/response models
```

**Structure Decision**: The implementation follows Option 2 (Web application) pattern with Docusaurus (frontend) components integrated into the book website. The chatbot UI components will be React components integrated into the Docusaurus site. The backend services already exist as part of the existing RAG infrastructure and will be extended to support the new UI requirements.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [None identified] | [N/A] | [N/A] |
