---
id: 0002
title: Update Project Constitution for Physical AI & Humanoid Robotics
stage: constitution
date: 2025-12-07
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: user
command: /sp.constitution Project: Docusaurus-based book “Physical AI & Humanoid Robotics” with an integrated RAG chatbot
labels: ["constitution", "update"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:

---

## Prompt

```text

/sp.constitution

Project: Docusaurus-based book “Physical AI & Humanoid Robotics” with an integrated RAG chatbot

Core principles:
- Technical accuracy across AI, robotics, and simulation
- Clear explanations for intermediate learners
- Reproducible steps for book generation, deployment, and chatbot setup
- Consistent structure aligned with Spec-Kit Plus and Claude Code workflows

Key standards:
- All descriptions must be correct for ROS 2, Gazebo, Unity, NVIDIA Isaac, Whisper, VSLAM, Nav2, and RAG systems
- Code and configuration examples must be runnable
- Chapters must align with the four modules and final capstone
- Chatbot must follow OpenAI Agents/ChatKit SDK patterns with FastAPI, Neon, and Qdrant
- Content must stay coherent across the whole book

Constraints:
- Format: Docusaurus book generated with Spec-Kit Plus
- Deployment: GitHub Pages with embedded RAG chatbot
- Chatbot responses must rely only on book content or selected text
- Coverage: all four modules plus a reproducible capstone walkthrough

Success criteria:
- Book builds and deploys without errors
- RAG chatbot retrieval and answering work end to end
- Readers can run ROS 2 basics, simulations, and perception pipelines
- Capstone humanoid simulation can be reproduced from the book alone
```

## Response snapshot

Updated the project constitution to version 0.1.0, incorporating new key standards and a more specific project description.

## Outcome

- ✅ Impact: Constitution updated.
- 🧪 Tests: No tests run.
- 📁 Files: `.specify/memory/constitution.md` modified.
- 🔁 Next prompts: Review updated constitution and dependent templates.
- 🧠 Reflection: Constitution updated successfully with minor version bump due to new content.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): None
- Prompt variant (if applicable): None
- Next experiment (smallest change to try): None
