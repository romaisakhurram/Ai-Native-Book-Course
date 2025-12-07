<!--
Sync Impact Report:
- Version change: 0.0.0 → 1.0.0
- List of modified principles:
  - [PRINCIPLE_1_NAME] → I. Technical Accuracy
  - [PRINCIPLE_2_NAME] → II. Clear Explanations
  - [PRINCIPLE_3_NAME] → III. Reproducibility
  - [PRINCIPLE_4_NAME] → IV. Consistent Structure
- Added sections:
  - Key Standards
  - Constraints and Success Criteria
- Removed sections: None
- Templates requiring updates:
  - ✅ .specify/templates/plan-template.md
  - ✅ .specify/templates/spec-template.md
  - ✅ .specify/templates/tasks-template.md
  - ✅ .claude/commands/sp.plan.md
- Follow-up TODOs: None
-->
# Physical AI & Humanoid Robotics Constitution

## Core Principles

### I. Technical Accuracy
Technical accuracy across AI, robotics, and simulation is paramount. All descriptions must be correct for ROS 2, Gazebo, Unity, NVIDIA Isaac, Whisper, VSLAM, Nav2, and RAG systems.

### II. Clear Explanations
The content must provide clear explanations for intermediate learners, ensuring complex topics are accessible without sacrificing technical depth.

### III. Reproducibility
All code and configuration examples must be runnable. Readers must be able to reproduce the book generation, deployment, chatbot setup, and the final capstone humanoid simulation from the provided steps alone.

### IV. Consistent Structure
The project must maintain a consistent structure aligned with Spec-Kit Plus and Claude Code workflows to ensure predictability and maintainability. Chapters must align with the four modules and the final capstone.

## Key Standards

- **Correctness:** All descriptions must be correct for ROS 2, Gazebo, Unity, NVIDIA Isaac, Whisper, VSLAM, Nav2, and RAG systems.
- **Runnability:** Code and configuration examples must be runnable.
- **Alignment:** Chapters must align with the four modules and final capstone.
- **Chatbot Pattern:** The chatbot must follow OpenAI Agents/ChatKit SDK patterns with FastAPI, Neon, and Qdrant.
- **Coherence:** Content must stay coherent across the whole book.

## Constraints and Success Criteria

### Constraints
- **Format:** Docusaurus book generated with Spec-Kit Plus.
- **Deployment:** GitHub Pages with embedded RAG chatbot.
- **Chatbot Scope:** Chatbot responses must rely only on book content or selected text.
- **Coverage:** The book must cover all four modules plus a reproducible capstone walkthrough.

### Success Criteria
- The book builds and deploys without errors.
- The RAG chatbot retrieval and answering work end-to-end.
- Readers can run ROS 2 basics, simulations, and perception pipelines.
- The capstone humanoid simulation can be reproduced from the book alone.

## Governance

Amendments to this constitution require a documented proposal, review, and an approved migration plan. All development artifacts and pull requests must verify compliance with these principles. Complexity must be justified, and deviations require explicit sign-off.

**Version**: 1.0.0 | **Ratified**: 2025-12-07 | **Last Amended**: 2025-12-07