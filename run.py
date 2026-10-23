# run.py
import os
from acrochoreo.orchestrator import app

def run_training_session():
    # 1. Read your 3 moves from your local text file
    moves_file = "moves.txt"
    if not os.path.exists(moves_file):
        # Create a sample file if it doesn't exist yet
        with open(moves_file, "w") as f:
            f.write("pirouette_right, sidesplit_right, highkick_right")
            
    with open(moves_file, "r") as f:
        moves_content = f.read().strip()
        # Split string by comma and clean whitespace
        target_moves = [move.strip() for move in moves_content.split(",") if move.strip()]

    print(f"📦 Loaded routine from file: {target_moves}")

    # 2. Set up a unique thread ID for this specific routine
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
    # The graph will run 'init_session' and instantly FREEZE at your human checkpoint
    app.invoke(initial_state, config=config)

    # 4. Check that the graph is waiting for you
    current_state = app.get_state(config)
    print(f"⏸️ Graph Interrupted successfully! It is paused at node: '{current_state.next[0]}'")
    print(f"📈 Current Version: {current_state.values['current_version']}")

    # --- SIMULATED GYM WORKOUT ---
    print("\n🏋️ [Imagine you just went to your home gym and practiced this sequence] 🏋️")
    human_notes = "Felt stable spinning right into the pirouette. The landing was clean but dropping instantly into the sidesplit caused tension in my hip flexor. Highkick was snappy."
    # -----------------------------

    # 5. Inject your real-world training notes directly back into the state machine
    gym_log = {
        "version": current_state.values["current_version"],
        "human_notes": human_notes,
        "status": "done" # Set to 'retry' if you wanted to generate a version 2 loop
    }

    print("\n📝 Updating state ledger with your gym notes...")
    app.update_state(config, {"version_history": [gym_log]}, as_node="human_checkpoint")

    print("🤖 Processing notes with AI Agent...")
    # Resume execution. The AI processor analyzes your raw notes and auto-tags them!
    final_output = app.invoke(None, config=config)

    # 6. Display the final version-controlled journal entry
    print("\n✅ Journal Session Finalized and Versioned!")
    print(f"🏷️ Semantic Search Tags Generated: {final_output['system_tags']}")
    print(f"📖 History Summary: Saved Version {final_output['current_version']} to memory.")

if __name__ == "__main__":
    run_training_session()
