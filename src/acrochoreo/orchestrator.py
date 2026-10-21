from langgraph.graph import StateGraph, END
from typing import TypedDict, Literal

class TaskState(TypedDict):
    task: str
    result: str
    attempts: int
    max_attempts: int

def choreograph(state: TaskState) -> TaskState:
    """Model decides which specialist handles this task."""
    from acrochoreo.llm_client import ask_ai
    choice = ask_ai(
        f"Task: {state['task']}. "
        f"Choose which specialist handles it: A (creative) or B (analytical). "
        f"Answer A or B."
    )
    return {**state, "next": "A" if "A" in choice else "B"}

def specialist_a(state: TaskState) -> TaskState:
    """Creative specialist."""
    from acrochoreo.llm_client import ask_ai
    result = ask_ai(f"[Creative] {state['task']}")
    return {**state, "result": result, "attempts": state["attempts"] + 1}

def specialist_b(state: TaskState) -> TaskState:
    """Analytical specialist."""
    from acrochoreo.llm_client import ask_ai
    result = ask_ai(f"[Analytical] {state['task']}")
    return {**state, "result": result, "attempts": state["attempts"] + 1}

def should_continue(state: TaskState) -> Literal["continue", "done"]:
    """Model judges if result is ready for show."""
    if state["attempts"] >= state["max_attempts"]:
        return "done"
    from acrochoreo.llm_client import ask_ai
    verdict = ask_ai(
        f"Result: {state['result']}. "
        f"Ready for show? Answer CONTINUE or STOP."
    )
    return "continue" if "CONTINUE" in verdict.upper() else "done"

workflow = StateGraph(TaskState)
workflow.add_node("choreograph", choreograph)
workflow.add_node("specialist_a", specialist_a)
workflow.add_node("specialist_b", specialist_b)
workflow.set_entry_point("choreograph")

def route_to_specialist(state: TaskState) -> Literal["specialist_a", "specialist_b"]:
    return "specialist_a" if "A" in state.get("next", "B") else "specialist_b"

workflow.add_conditional_edges("choreograph", route_to_specialist)
workflow.add_edge("specialist_a", "choreograph")
workflow.add_edge("specialist_b", "choreograph")
workflow.add_conditional_edges("choreograph", should_continue, {"continue": "choreograph", "done": END})

app = workflow.compile()