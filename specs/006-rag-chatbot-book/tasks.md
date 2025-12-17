---

description: "Task list for RAG Chatbot implementation"
---

# Tasks: Integrated RAG Chatbot for Markdown Book

**Input**: Design documents from `/specs/006-rag-chatbot-book/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `frontend/src/`
- **Backend service**: `backend/` at repository root
- Paths shown below assume backend service structure from plan.md

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create backend directory structure per implementation plan
- [x] T002 Initialize Python project with uv in backend/
- [x] T003 [P] Install FastAPI, OpenAI SDK, Qdrant client, Neon connector, python-dotenv dependencies
- [x] T004 Create .env file template with API key placeholders
- [x] T005 Create basic project configuration in backend/config/settings.py

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T006 Setup database models in backend/models/database.py
- [x] T007 [P] Create Pydantic schemas for all entities in backend/models/schemas.py
- [x] T008 [P] Setup Qdrant client and collection configuration in backend/services/embedding_service.py
- [x] T009 Setup Neon Postgres connection in backend/models/database.py
- [x] T010 Create base API structure in backend/main.py with dependencies
- [x] T011 Setup middleware for request handling in backend/middleware/

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Ask Questions and Receive Answers from Book Content (Priority: P1) 🎯 MVP

**Goal**: Enable users to ask questions about book content and receive answers based on semantic search over the full book

**Independent Test**: Can be fully tested by asking questions about a specific topic in the book and verifying that the chatbot returns accurate answers based on the book content.

### Implementation for User Story 1

- [x] T012 [P] [US1] Create Book Content Chunk model in backend/models/models.py
- [x] T013 [P] [US1] Create Chat Session model in backend/models/models.py
- [x] T014 [P] [US1] Create Query and Response models in backend/models/models.py
- [x] T015 [US1] Implement content parsing and chunking in backend/services/content_processor.py
- [x] T016 [US1] Implement embedding generation for book content in backend/services/embedding_service.py
- [x] T017 [US1] Implement semantic search in backend/services/retrieval_service.py
- [x] T018 [US1] Implement chat generation in backend/services/chat_service.py
- [x] T019 [US1] Create session endpoint in backend/api/routes/sessions.py
- [x] T020 [US1] Create queries endpoint in backend/api/routes/queries.py
- [x] T021 [US1] Integrate retrieval and chat services in query processing

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Ask Questions Based on Selected Text Only (Priority: P2)

**Goal**: Enable users to highlight specific text in the book and ask questions that are answered only from that selected text, rather than the entire book

**Independent Test**: Can be tested by selecting text, asking a question related to that text, and verifying that the answer is limited to information from the selected text.

### Implementation for User Story 2

- [x] T022 [P] [US2] Update Query model to include selected text in backend/models/models.py
- [x] T023 [P] [US2] Create User Selection model in backend/models/models.py
- [x] T024 [US2] Implement selected-text mode in backend/services/retrieval_service.py
- [x] T025 [US2] Update chat service to handle selected-text context in backend/services/chat_service.py
- [x] T026 [US2] Update API endpoints to support selected-text queries in backend/api/routes/queries.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Persist Chat Sessions and History (Priority: P3)

**Goal**: Save chat sessions and metadata so users can resume conversations later and review previous interactions

**Independent Test**: Can be tested by starting a conversation, leaving the book, and then returning to continue the conversation or view history.

### Implementation for User Story 3

- [x] T027 [P] [US3] Update Chat Session model with persistence fields in backend/models/models.py
- [x] T028 [US3] Implement session persistence in backend/utils/db_operations.py
- [x] T029 [US3] Add query/response storage in backend/utils/db_operations.py
- [x] T030 [US3] Update API endpoints to retrieve session history in backend/api/routes/sessions.py
- [x] T031 [US3] Implement session management including retrieval and cleanup

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Frontend Integration

**Goal**: Embed the chatbot UI into the Docusaurus book interface

- [x] T032 [P] Create frontend files and structure in frontend/
- [x] T033 Create ChatInterface component in frontend/src/components/ChatInterface.jsx
- [x] T034 Implement text selection handling in frontend/src/utils/selection.js
- [x] T035 Integrate ChatInterface with Docusaurus pages via documentation
- [x] T036 Add communication between frontend and backend API
- [x] T037 Test end-to-end functionality between frontend and backend

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T038 [P] Add comprehensive logging across all services
- [x] T039 Add rate limiting and error handling middleware
- [x] T040 [P] Write API documentation based on OpenAPI contract
- [x] T041 Add security measures for API endpoints
- [x] T042 Performance optimization for embedding and retrieval
- [x] T043 Run quickstart.md validation for complete setup
- [x] T044 Update all documentation with final implementation details

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Frontend Integration (Phase 6)**: Depends on all backend user stories being complete
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Builds on US1 services
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Builds on US1 services

### Within Each User Story

- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all models for User Story 1 together:
Task: "Create Book Content Chunk model in backend/models/schemas.py"
Task: "Create Chat Session model in backend/models/schemas.py"
Task: "Create Query and Response models in backend/models/schemas.py"
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
5. Add Frontend Integration → Test end-to-end → Deploy/Demo
6. Each addition adds value without breaking previous functionality

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Frontend developer: Can work on Phase 6 concurrently
4. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence