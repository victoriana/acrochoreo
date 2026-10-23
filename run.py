# run.py
import os
import sys
import argparse

# Ensure Python looks inside the src directory for your imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

from acrochoreo.orchestrator import app

MOVES_FILE = "moves.txt"

def load_moves():
    """Helper to read moves from disk into a clean list."""
    if not os.path.exists(MOVES_FILE):
        return []
    with open(MOVES_FILE, "r") as f:
        content = f.read().strip()
        if not content:
            return []
        return [move.strip() for move in content.split(",") if move.strip()]

def save_moves(moves):
    """Helper to write a list of moves back to disk as a comma-separated line."""
    with open(MOVES_FILE, "w") as f:
        f.write(", ".join(moves))

def get_multiline_input(prompt_text):
    print(prompt_text)
    print("(Press Enter, then Ctrl-D or Ctrl-Z on Windows to save your input)")
    return sys.stdin.read().strip()

# --- CLI COMMAND FUNCTIONS ---

def cmd_show(args):
    moves = load_moves()
    if not moves:
        print("📭 Your sequence is currently empty!")
    else:
        print(f"📋 Current Active Sequence: {' -> '.join(moves)}")

def cmd_add(args):
    moves = load_moves()
    new_move = args.move.strip()
    moves.append(new_move)
    save_moves(moves)
    print(f"✅ Added '{new_move}' to your sequence.")
    print(f"📋 New Sequence: {' -> '.join(moves)}")

def cmd_remove(args):
    moves = load_moves()
    target_move = args.move.strip()
    if target_move not in moves:
        print(f"❌ Error: '{target_move}' is not in your current sequence.")
        return
    moves.remove(target_move)
    save_moves(moves)
    print(f"🗑️ Removed '{target_move}' from your sequence.")
    print(f"📋 New Sequence: {' -> '.join(moves)}")

def cmd_replace(args):
    moves = load_moves()
    old_move = args.old.strip()
    new_move = args.new.strip()
    if old_move not in moves:
        print(f"❌ Error: '{old_move}' is not in your current sequence.")
        return
    # Find index and swap it out
    idx = moves.index(old_move)
    moves[idx] = new_move
    save_moves(moves)
    print(f"🔄 Swapped '{old_move}' with '{new_move}'.")
    print(f"📋 New Sequence: {' -> '.join(moves)}")

def cmd_start(args):
    target_moves = load_moves()
    if not target_moves:
        print("❌ Cannot start session: Your sequence file is empty. Add some moves first!")
        return

    print(f"📦 Loaded routine from file: {target_moves}")
    config = {"configurable": {"thread_id": "routine_session_v1"}}

    initial_state = {
        "sequence_id": "seq_001",
        "target_moves": target_moves,
        "version_history": [],
        "current_version": 0,
        "system_tags": []
    }

    print("\n🚀 Initializing journal session in LangGraph...")
    app.invoke(initial_state, config=config)

    current_state = app.get_state(config)
    print(f"⏸️ Graph Interrupted successfully! Paused at node: '{current_state.next}'")
    print(f"📈 Current Version Entry: {current_state.values['current_version']}")

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
    status_input = input("🔄 Practice/retry this again next session? (yes/no): ").strip().lower()
    status = "retry" if status_input in ["yes", "y"] else "done"
    print("="*60)

    combined_notes = f"[Physical Execution Log]: {exec_notes}\n[Evaluation & Critique]: {eval_notes}"
    gym_log = {
        "version": current_state.values["current_version"],
        "human_notes": combined_notes,
        "status": status
    }

    print("\n¼📝 Updating state ledger with your structured notes...")
    app.update_state(config, {"version_history": [gym_log]}, as_node="human_checkpoint")

    print("🤖 Processing notes with AI Agent...")
    final_output = app.invoke(None, config=config)

    print("\n✅ Journal Session Finalized and Versioned!")
    print(f"🏷️ Semantic Search Tags Generated: {final_output['system_tags']}")
    print(f"📖 History Summary: Saved Version {final_output['current_version']} to memory.")

# --- MAIN PARSER ENTRYPOINT ---

def main():
    parser = argparse.ArgumentParser(description="Acrochoreo: CLI Move Tracker & Agentic Journal")
    subparsers = parser.add_subparsers(dest="command", required=True, help="Available subcommands")

    # Show command
    subparsers.add_parser("show", help="Display the active acrobatic move sequence")

    # Add command
    parser_add = subparsers.add_parser("add", help="Append a new move to the sequence")
    parser_add.add_argument("move", type=str, help="Name of the move to append")

    # Remove command
    parser_remove = subparsers.add_parser("remove", help="Delete a specific move from the sequence")
    parser_remove.add_argument("move", type=str, help="Name of the move to strip out")

    # Replace command
    parser_replace = subparsers.add_parser("replace", help="Swap an existing move for a new one")
    parser_replace.add_argument("old", type=str, help="Name of the move to be replaced")
    parser_replace.add_argument("new", type=str, help="Name of the new move replacing it")

    # Start command
    subparsers.add_parser("start", help="Boot up the interactive LangGraph journal session")

    args = parser.parse_args()

    # Map subcommands to handling functions
    commands = {
        "show": cmd_show,
        "add": cmd_add,
        "remove": cmd_remove,
        "replace": cmd_replace,
        "start": cmd_start
    }

    commands[args.command](args)

if __name__ == "__main__":
    main()
