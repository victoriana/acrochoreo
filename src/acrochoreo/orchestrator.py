import json
import os
from typing import TypedDict, List, Dict

# The exact State Schema you planned
class JournalState(TypedDict):
    sequence_id: str
    target_moves: List[str]
    version_history: List[Dict]
    current_version: int
    system_tags: List[str]

class PureAgenticEngine:
    """A compilation-free agentic engine that tracks state history natively."""
    def __init__(self, ledger_file: str = "journal_ledger.json"):
        self.ledger_file = ledger_file

    def _load_ledger(self) -> Dict:
        if os.path.exists(self.ledger_file):
            with open(self.ledger_file, "r") as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return {}
        return {}

    def _save_ledger(self, thread_id: str, state: dict):
        ledger = self._load_ledger()
        ledger[thread_id] = state
        with open(self.ledger_file, "w") as f:
            json.dump(ledger, f, indent=4)

    def get_state(self, config: dict) -> dict:
        thread_id = config.get("configurable", {}).get("thread_id", "default")
        ledger = self._load_ledger()
        return ledger.get(thread_id, None)

    def update_state(self, config: dict, state_update: dict, as_node: str = None):
        thread_id = config.get("configurable", {}).get("thread_id", "default")
        current = self.get_state(config) or {}
        
        # Merge arrays cleanly if they exist in updates
        if "version_history" in state_update and "version_history" in current:
            current["version_history"].extend(state_update["version_history"])
        else:
            current.update(state_update)
            
        self._save_ledger(thread_id, current)

    def invoke(self, initial_state: dict = None, config: dict = None) -> dict:
        thread_id = config.get("configurable", {}).get("thread_id", "default")
        
        # 1. Initialization Node
        if initial_state is not None:
            state = {
                "sequence_id": initial_state.get("sequence_id", "seq_001"),
                "target_moves": initial_state.get("target_moves", []),
                "version_history": initial_state.get("version_history", []),
                "current_version": len(initial_state.get("version_history", [])) + 1,
                "system_tags": initial_state.get("system_tags", [])
            }
            self._save_ledger(thread_id, state)
            print(f"📈 Current Version Entry set to: {state['current_version']}")
            return state # Gracefully yield control back to terminal for the Human Checkpoint

        # 2. Resuming Execution -> Agentic AI Processing Node
        state = self.get_state(config)
        if not state or not state.get("version_history"):
            return state

        from acrochoreo.llm_client import ask_ai
        latest_history = state["version_history"][-1]
        human_notes = latest_history.get("human_notes", "")

        print("🤖 Processing notes with AI Agent...")
        ai_analysis = ask_ai(
            f"Analyze this acrobatic journal entry for sequence {state['target_moves']}.\n"
            f"Human Notes: {human_notes}\n"
            f"Generate 3-4 comma-separated search tags (e.g., balance-issue, fluid-transition, hip-flexibility)."
        )

        # Clean and append tags natively
        new_tags = [tag.strip().lower() for tag in ai_analysis.split(",") if tag.strip()]
        state["system_tags"] = list(set(state.get("system_tags", []) + new_tags))
        
        # Conditional Route Engine: increment version if human selected retry
        if latest_history.get("status") == "retry":
            state["current_version"] += 1
            
        self._save_ledger(thread_id, state)
        return state

# Export an identically named instance so run.py continues to compile seamlessly!
app = PureAgenticEngine()
