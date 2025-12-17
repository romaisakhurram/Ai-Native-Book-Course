---

description: "Task list for embedded RAG chatbot UI implementation"
---

# Tasks: Embedded RAG Chatbot UI for Book Website

**Input**: Design documents from `/specs/007-chatbot-ui/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The feature specification did not explicitly request tests, so this implementation will not include test tasks.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `docusaurus-book/src/` for frontend components, `backend/src/` for backend
- Paths adjusted based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project structure per implementation plan in docusaurus-book/
- [X] T002 Initialize React and Docusaurus project with required dependencies
- [X] T003 [P] Configure linting, formatting tools and TypeScript for frontend

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

Examples of foundational tasks (adjust based on your project):

- [X] T004 [P] Create ChatSession model in docusaurus-book/src/components/Chatbot/ChatSession.ts
- [X] T005 [P] Create Message model in docusaurus-book/src/components/Chatbot/Message.ts
- [X] T006 [P] Create MessageContext model in docusaurus-book/src/components/Chatbot/MessageContext.ts
- [X] T007 [P] Create ChatRequest model in docusaurus-book/src/components/Chatbot/ChatRequest.ts
- [X] T008 [P] Create ChatResponse model in docusaurus-book/src/components/Chatbot/ChatResponse.ts
- [X] T009 Set up session storage utility in docusaurus-book/src/utils/session-storage.ts
- [X] T010 Set up API service for chat endpoints in docusaurus-book/src/services/chat-api.ts

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Access and Use Embedded Chatbot (Priority: P1) 🎯 MVP

**Goal**: Create a floating chat launcher and slide-in chat panel that allows users to access a chatbot interface directly from any page of the book without reloading the page

**Independent Test**: Can be fully tested by accessing any book page, opening the chat interface, and having a basic conversation about the book content. This delivers immediate value by providing help without page changes or external tools.

### Implementation for User Story 1

- [X] T011 [P] [US1] Create ChatLauncher component in docusaurus-book/src/components/Chatbot/ChatLauncher.tsx
- [X] T012 [P] [US1] Create ChatPanel component in docusaurus-book/src/components/Chatbot/ChatPanel.tsx
- [X] T013 [P] [US1] Create ChatWindow component in docusaurus-book/src/components/Chatbot/ChatWindow.tsx
- [X] T014 [P] [US1] Create Message component in docusaurus-book/src/components/Chatbot/MessageComponent.tsx
- [X] T015 [US1] Implement chat panel open/close functionality in ChatLauncher.tsx
- [X] T016 [US1] Implement basic messaging in ChatWindow.tsx (send/receive messages)
- [X] T017 [US1] Integrate with API service to send messages to backend
- [X] T018 [US1] Style components to match book design aesthetic
- [X] T019 [US1] Ensure responsive design works for mobile and desktop
- [X] T020 [US1] Add accessibility features to chat components

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Ask Questions About Selected Text (Priority: P1)

**Goal**: Enable users to select specific text on a page and ask questions specifically about that text, with the selected text appearing in the chat context

**Independent Test**: Can be fully tested by selecting text on a page, opening the chat interface, and seeing the selected text in the context of the conversation. Then, asking a question about the selected text should yield a relevant response.

### Implementation for User Story 2

- [X] T021 [P] [US2] Create SelectionHandler utility in docusaurus-book/src/components/Chatbot/SelectionHandler.ts
- [X] T022 [P] [US2] Add text selection detection to docusaurus-book/src/components/Chatbot/ChatWindow.tsx
- [X] T023 [US2] Implement selected text display in chat context
- [X] T024 [US2] Update ChatRequest model to include selected text context
- [X] T025 [US2] Implement backend endpoint to handle selected text context in backend/src/api/v1/endpoints/chat.py
- [X] T026 [US2] Update chat API service to include selected text in requests
- [X] T027 [US2] Update backend RAG service to use selected text as context (backend/src/core/rag_service.py)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Session-Based Chat History Persistence (Priority: P2)

**Goal**: Ensure chat history persists during a user's session as they navigate between book pages, with an option to clear chat history

**Independent Test**: Can be tested by having a conversation with the chatbot, navigating to a different page, and then continuing the conversation with context preserved. This delivers value by allowing continuous learning without repetition.

### Implementation for User Story 3

- [X] T028 [P] [US3] Enhance session storage utility to handle chat history in docusaurus-book/src/utils/session-storage.ts
- [X] T029 [US3] Implement chat session management in docusaurus-book/src/components/Chatbot/ChatWindow.tsx
- [X] T030 [US3] Add functionality to retrieve chat history on page load
- [X] T031 [US3] Add clear chat history functionality
- [X] T032 [US3] Implement session persistence across page navigations
- [ ] T033 [US3] Update backend to maintain session context across requests

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Streaming Responses (Priority: P1)

**Goal**: Implement streaming responses to provide immediate feedback to users, with the initial text delivered within 1 second of query submission

**Independent Test**: Verify that responses from the chatbot are streamed in real-time rather than displayed all at once, with the first token appearing within 1 second of submitting the query.

### Implementation for Streaming Responses

- [ ] T034 [P] [STREAM] Update backend to support Server-Sent Events in backend/src/api/v1/endpoints/chat.py
- [ ] T035 [STREAM] Implement SSE client in docusaurus-book/src/services/chat-api.js
- [ ] T036 [STREAM] Update ChatWindow component to handle streaming responses in docusaurus-book/src/components/Chatbot/ChatWindow.jsx
- [ ] T037 [STREAM] Add UI indicators for streaming state
- [ ] T038 [STREAM] Handle streaming state in Message component

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T039 [P] Integrate chatbot UI with Docusaurus in docusaurus-book/docusaurus.config.js
- [ ] T040 [P] Update main App layout to include ChatLauncher in docusaurus-book/src/pages/layout.js
- [ ] T041 Update backend models to support chat session requirements in backend/src/models/chat_models.py
- [ ] T042 Error handling and graceful degradation for API failures
- [ ] T043 [P] Documentation updates for chatbot integration
- [ ] T044 Performance optimization for chat components
- [ ] T045 Run quickstart.md validation to ensure deployment works properly
- [ ] T046 Add loading indicators and improve UX for better user experience
- [ ] T047 Add keyboard shortcuts for improved accessibility

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable
- **Streaming Responses**: Can start after Foundational (Phase 2) - Core functionality but enhances all user stories

### Within Each User Story

- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all models for User Story 1 together:
Task: "Create ChatLauncher component in docusaurus-book/src/components/Chatbot/ChatLauncher.jsx"
Task: "Create ChatPanel component in docusaurus-book/src/components/Chatbot/ChatPanel.jsx"
Task: "Create ChatWindow component in docusaurus-book/src/components/Chatbot/ChatWindow.jsx"
Task: "Create Message component in docusaurus-book/src/components/Chatbot/Message.jsx"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add Streaming → Test independently → Deploy/Demo
6. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
   - Developer D: Streaming Responses
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence