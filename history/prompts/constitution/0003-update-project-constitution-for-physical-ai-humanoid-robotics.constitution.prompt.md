---
id: 0003
title: Update Project Constitution for Physical AI Humanoid Robotics
stage: constitution
date: 2025-12-07
surface: agent
model: gemini
feature: none
branch: master
user: User
command: /sp.constitution
labels: ["constitution", "governance", "documentation"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
- .specify/memory/constitution.md
- .specify/templates/plan-template.md
tests:
- "none"
---

## Prompt

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

## Response snapshot

I have updated the project constitution to version 1.0.0, establishing the initial governance based on the principles you provided. I also updated the planning template (`.specify/templates/plan-template.md`) to ensure all future development aligns with these new standards.

Here is a suggested commit message:
`docs: initialize constitution v1.0.0`

## Outcome

- ✅ Impact: TODO
- 🧪 Tests: n/a
- 📁 Files: 2 files modified
- 🔁 Next prompts: n/a
- 🧠 Reflection: n/a

## Evaluation notes (flywheel)

- Failure modes observed: n/a
- Graders run and results (PASS/FAIL): n/a
- Prompt variant (if applicable): n/a
- Next experiment (smallest change to try): n/a
