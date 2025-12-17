# Implementation Plan: Book Module 1 - The Robotic Nervous System (ROS 2)

**Branch**: `001-book-module-1-ros2` | **Date**: 2025-12-15 | **Spec**: [./spec.md](./spec.md)
**Input**: Feature specification from `specs/001-book-module-1-ros2/spec.md`

## Summary

This plan outlines the architecture for Module 1 of the AI-Native Book Course: "The Robotic Nervous System (ROS 2)". The module focuses on teaching ROS 2 concepts using humanoid robots as continuous examples throughout. It includes a Preface explaining the course vision, clear chapter structure (Intro → Architecture → Coding → URDF), and integration of at least three diagrams explaining ROS 2 data flow. The content follows textbook-style tone with runnable Python (rclpy) examples and URDF snippets, all authored in Docusaurus markdown format.

## Technical Context

**Language/Version**: JavaScript (Docusaurus), Python 3.10+ (ROS 2 Humble Hawksbill)
**Primary Dependencies**: Docusaurus, React, ROS 2 Humble Hawksbill, rclpy, Markdown
**Storage**: N/A (documentation project with embedded examples)
**Testing**:
- Docusaurus builds validation.
- Manual and automated checks for code example correctness.
- Verification of ROS 2 example execution (under 5 seconds).
- Validation of URDF file syntax and functionality.
**Target Platform**: Web (statically generated site deployable to GitHub Pages).
**Project Type**: Documentation (Docusaurus-based book with embedded examples).
**Performance Goals**: ROS 2 code examples must run in under 5 seconds on standard hardware.
**Constraints**: Examples must follow ROS 2 security best practices, content must be textbook-style, must include diagrams (Mermaid or ASCII).
**Scale/Scope**: Module 1 book content with 2-3 chapters, runnable code examples, URDF snippets.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] **I. Technical Accuracy**: The plan emphasizes validating all technical descriptions and examples against ROS 2, Gazebo, and other specified technologies.
- [x] **II. Clear Explanations**: The Docusaurus structure is well-suited for clear explanations and navigation for intermediate learners.
- [x] **III. Reproducibility**: The plan includes a workflow for writing, reviewing, and testing code examples to ensure they are runnable.
- [x] **IV. Consistent Structure**: The project will adhere to Spec-Kit Plus and a phased approach, ensuring a consistent and maintainable structure. Chapters will map to specs.

## Project Structure

### Documentation (this feature)

```text
specs/001-book-module-1-ros2/
├── plan.md              # This file
├── research.md          # To be created in Phase 0
├── data-model.md        # To be created in Phase 1
├── quickstart.md        # To be created in Phase 1
├── contracts/           # To be created in Phase 1
└── tasks.md             # To be created in Phase 2
```

### Source Code (repository root)

```text
# Docusaurus site
docs/
├── preface.md           # Course vision, prerequisites, and usage guide
├── module1/             # Module 1: The Robotic Nervous System (ROS 2)
│   ├── 00-intro.md      # Introduction to ROS 2 as the nervous system
│   ├── 01-architecture.md # ROS 2 architecture, nodes, topics, services, actions
│   ├── 02-coding.md     # rclpy coding with humanoid robot examples
│   └── 03-urdf.md       # Humanoid URDF structure and examples
├── module2/
├── module3/
└── capstone/

# ROS 2 Examples
src/ros2_examples/
├── simple_talker.py     # Publisher example with comprehensive comments
├── simple_listener.py   # Subscriber example with comprehensive comments
├── simple_service.py    # Service example with comprehensive comments
├── simple_client.py     # Client example with comprehensive comments
├── humanoid_controller.py # Complete Python ROS 2 node example with comments
└── test_examples.py     # Unit tests for examples

# URDF Files
src/urdf/
├── simple_humanoid.urdf # Simplified humanoid URDF snippet with explanation
└── full_humanoid.urdf   # Complete humanoid model

# Docusaurus project files
src/
├── components/
│   └── Chatbot.js
├── css/
└── pages/
docusaurus.config.js
sidebars.js

# Diagrams
static/img/
├── ros2_architecture.mmd # Mermaid diagram of ROS 2 architecture
├── ros2_communication.mmd # Mermaid diagram of communication model
└── humanoid_control.mmd # Mermaid diagram of humanoid control pipeline
```

**Structure Decision**: The project will consist of a Docusaurus website for the book content with structured modules. Each module will have chapters with textbook-style explanations, code examples embedded as fenced code blocks, and diagrams to illustrate concepts. The ROS 2 examples will be kept in src/ros2_examples/ with unit tests.

## Navigation and Content Structure

1.  **Preface Creation**: Create a comprehensive preface explaining course vision, Physical AI context, prerequisites, and how to navigate the book.
2.  **Module Structure**: Define Module 1 chapter structure as: Introduction → ROS 2 Architecture → rclpy Coding → Humanoid URDF.
3.  **Continuous Example**: Use a humanoid robot as the continuous example throughout all chapters.
4.  **Navigation Behavior**: Implement hover behavior on "Module 1 – The Robotic Nervous System" to first display the module heading, then expand to show its chapters.
5.  **Diagram Integration**: Place at least three diagrams explaining ROS 2 data flow and humanoid control pipelines in strategic locations.

## Content Requirements

1.  **Python Example**: Include one complete Python (rclpy) ROS 2 node example with comprehensive comments for student understanding.
2.  **URDF Snippet**: Include one simplified humanoid URDF snippet with clear explanation of components.
3.  **Textbook Tone**: Ensure all content follows textbook-style instructional tone appropriate for students with basic Python knowledge.
4.  **Docusaurus Markdown**: Author all content in Docusaurus markdown structure for proper rendering.

## Decisions for Documentation

The following architectural decisions will be documented in `research.md` or ADRs:

- **Module Structure**: The decision to organize Module 1 into 4 distinct chapters: Intro → Architecture → Coding → URDF.
- **Humanoid Robot Focus**: Using humanoid robots as the continuous example throughout the module.
- **Diagram Strategy**: Using Mermaid/ASCII diagrams to explain ROS 2 concepts and data flow.
- **Code Example Standards**: Ensuring all ROS 2 code examples run in under 5 seconds with security best practices.

## Complexity Tracking

No violations of the constitution are anticipated.