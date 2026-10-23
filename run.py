# run.py
import os
import sys

# Ensure Python looks inside the src directory for your imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

from acrochoreo.orchestrator import app

def get_multiline_input(prompt_text):
    print(prompt_text)
    print("(Press Enter, then Ctrl-D or Ctrl-Z on Windows to save your input)")
    lines = sys.stdin.read().strip()
    return lines

def run_training_session():
    # 1. Read your 3 moves from your local text file
    moves_file = "moves.txt"
    if not os.path.exists(moves_file):
        with open(moves_file, "w") as f:
            f.write("pirouette_right, sidesplit_right, highkick_right")
            
    with open(moves_file, "r") as f:
        moves_content = f.read().strip()
        target_moves = [move.strip() for move in moves_content.split(",") if move.strip()]

    print(f"📦 Loaded routine from file: {target_moves}")

    # 2. Set up a unique thread ID for this specific routine session
    config = {"configurable": {"thread_id": "routine_pirouette_split_v1"}}

    # 3. Initialize your journal state ledger
    initial_state = {
        "sequence_id": "seq_001",
        "target_moves": target_moves,
        "version_history": [],
        "current_version": 0,
        "system_tags": []
    }

    print("\n🚀 Initializing journal session in LangGraph...")
    app.invoke(initial_state, config=config)

    # 4. Check that the graph is waiting for you
    current_state = app.get_state(config)
    print(f"⏸️ Graph Interrupted successfully! Paused at node: '{current_state.next}'")
    print(f"📈 Current Version Entry: {current_state.values['current_version']}")

    # --- HYPER-CLEAR INTERACTIVE PROMPTS ---
    print("\n" + "="*60)
    print("📋 STEP 1: PHYSICAL EXECUTION LOG")
    print("="*60)
    exec_notes = get_multiline_input(
        "Describe how you physically executed the sequence.\n"
        "Consider: Balance, stability, transition speed, and spatial awareness."
    )

    print("\n" + "="*60)
    print("📋 STEP 2: CRITIQUE & EVALUATION")
    print("="*60)
    eval_notes = get_multiline_input(
        "Provide your evaluation and subjective assessment.\n"
        "Consider: Tightness/pain, fluidness, rhythm, or changes for next time."
    )
    
    print("\n" + "="*60)
    status_input = input("🔄 Would you like to practice/retry this again next session? (yes/no): ").strip().lower()
    status = "retry" if status_input in ["yes", "y"] else "done"
    print("="*60)
    # -----------------------------------

    # Combine both clean perspectives into a single unified journal payload for the AI
    combined_notes = (
        f"[Physical Execution Log]: {exec_notes}\n"
        f"[Evaluation & Critique]: {eval_notes}"
    )

    gym_log = {
        "version": current_state.values["current_version"],
        "human_notes": combined_notes,
        "status": status
    }

    print("\n📝 Updating state ledger with your structured notes...")
    app.update_state(config, {"version_history": [gym_log]}, as_node="human_checkpoint")

    print("🤖 Processing notes with AI Agent...")
    final_output = app.invoke(None, config=config)

    # 6. Display the final version-controlled journal entry
    print("\n✅ Journal Session Finalized and Versioned!")
    print(f"🏷️ Semantic Search Tags Generated: {final_output['system_tags']}")
    print(f"📖 History Summary: Saved Version {final_output['current_version']} to memory.")

if __name__ == "__main__":
    run_training_session()
