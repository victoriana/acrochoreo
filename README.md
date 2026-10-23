# Acrochoreo

Your personal training journal for building acrobatic sequences.

Acrochoreo helps you track your routine, log how it *felt* after practice, and automatically organize your progress so you can see exactly how your movement evolves over time.

## How It Works

The system combines a simple command-line interface for managing your choreography with an interactive session that captures your subjective feedback after every run-through.

### 1. Managing Your Routine
Build your sequence using simple commands:
- `show`: View your current active routine.
- `add <move>`: Append a new move to the end of your sequence.
- `remove <move>`: Delete a specific move from your routine.
- `replace <old> <new>`: Swap a difficult element for a regression or variation.

**Example Workflow:**
python run.py add "cartwheel"
python run.py add "front handspring"
python run.py replace "front handspring" "round-off back tuck"
python run.py show

### 2. The Training Session (`start`)
After practicing your routine, boot the interactive journaling mode to capture your performance:

1.  **Physical Execution Log:** Describe how the sequence *felt*. Note balance issues, transition speed, spatial awareness, or moments where you felt unstable.
2.  **Critique & Evaluation:** Provide your subjective assessment. Was the rhythm fluid? Did you feel tight in the hips? Did the handoff feel safe?
3.  **AI Analysis:** The system analyzes your notes to generate semantic tags (e.g., `balance-issue`, `fluid-transition`, `hip-flexibility`). This turns unstructured feelings into searchable data.
4.  **Versioning:** Your session is saved as a versioned entry. If you flag a "retry," the system automatically increments the version number, allowing you to compare v1 vs. v2 of the same sequence directly.

**Example Session:**

###python run.py start

### System prompts:

### 📋 STEP 1: PHYSICAL EXECUTION LOG
### Describe how you physically executed the sequence...
### > Felt unstable on the round-off, rushed the back tuck entry.

### 📋 STEP 2: CRITIQUE & EVALUATION  
### Provide your evaluation and subjective assessment...
### > Rhythm was choppy. Need to slow down the approach next time.

### 🔄 Practice/retry this again next session? (yes/no): yes

### ✅ Journal Session Finalized!
### 🏷️ Semantic Search Tags Generated: balance-issue, rushed-entry, rhythm-choppy
### 📖 History Summary: Saved Version 2 to memory.

## Key Features

-   **Memory Beyond Recall:** You don't have to remember why a transition failed three weeks ago. The system tags your sessions so you can search for past instances of specific issues.
-   **Human-Led Coaching:** The AI doesn't judge your form; it structures *your* judgment. You provide the insight; the system provides the organization.
-   **Sequence Evolution:** Track exactly when you swapped a move and why. See the history of your routine's development, not just its current state.
-   **Portable & Private:** Runs locally on your machine. Your training data stays with you.

## Related

-   [agentic-eval-harness](https://github.com/victoriana/agentic-eval-harness) — Evaluation harness that scores this system’s agent quality.
-   [github-actions-reusable-workflow](https://github.com/victoriana/github-actions-reusable-workflow) — CI/CD pipeline that integrates the eval harness as a governance gate.
