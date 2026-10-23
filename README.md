# Acrochoreo

A CLI-based agentic training journal that combines state-managed logging with AI-driven analysis.

Acrochoreo helps you build and refine acrobatic move sequences by combining a local JSON ledger with an AI agent that generates semantic tags for your training notes.

## How It Works

The system uses a **CLI interface** to manage sequences and an **interactive journaling session** to capture and analyze performance data.

### 1. Sequence Management
Manage your routine using simple commands:
- `show`: View your current active sequence.
- `add <move>`: Append a new move to the sequence.
- `remove <move>`: Delete a move from the sequence.
- `replace <old> <new>`: Swap one move for another.

### 2. Agentic Journaling (`start`)
Boot the interactive session to practice and record:
1.  **Execution Log:** Describe your physical performance (balance, stability, transitions).
2.  **Critique & Evaluation:** Provide subjective assessment (tightness, fluidity, rhythm).
3.  **AI Analysis:** The system processes your notes via an LLM to generate semantic search tags (e.g., `balance-issue`, `fluid-transition`).
4.  **Versioning:** Your session is saved as a versioned entry in the local ledger, with automatic version incrementing if a "retry" is flagged.

## Architecture

Acrochoreo implements a **single-node agentic engine** with native state management:

-   **PureAgenticEngine:** A lightweight, compilation-free engine that manages the `JournalState` schema.
-   **JSON Ledger:** All state (sequences, history, tags) is persisted in a local `journal_ledger.json` file.
-   **AI Integration:** The engine calls an LLM client (`ask_ai`) to analyze human notes and generate structured metadata (tags).
-   **Conditional Routing:** The engine automatically increments version numbers based on the user’s "retry" status.

## Key Features

-   **Native State Management:** Built from scratch using `TypedDict` and JSON persistence, avoiding external framework dependencies.
-   **Semantic Search:** AI-generated tags allow for easy retrieval of past sessions based on specific issues or successes.
-   **Human-in-the-Loop:** The system relies on human annotation for evaluation, with the AI providing structure and recall.
-   **CLI Interface:** Lightweight, portable, and easy to integrate into any workflow.

## Related

-   [agentic-eval-harness](https://github.com/victoriana/agentic-eval-harness) — Evaluation harness that scores this system’s agent quality.
-   [github-actions-reusable-workflow](https://github.com/victoriana/github-actions-reusable-workflow) — CI/CD pipeline that integrates the eval harness as a governance gate.


