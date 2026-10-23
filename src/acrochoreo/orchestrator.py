from langgraph.graph import StateGraph, END
from typing import TypedDict, Literal

class TaskState(TypedDict):
    task: str
    result: str
    attempts: int
    max_attempts: int
    status: Literal["continue", "done"]

def acrobat(state: TaskState) -> TaskState:
    """The solo worker executing the acrobatic sequences."""
    from acrochoreo.llm_client import ask_ai
    
    context = f"Task: {state['task']}"
    if state["result"]:
        context += f"\nPrevious attempt to refine: {state['result']}"
        
    result = ask_ai(f"[Acrobat worker] {context}")
    return {**state, "result": result, "attempts": state["attempts"] + 1}

def choreographer(state: TaskState) -> TaskState:
    """Combines routing & direction: judges readiness and sets the status."""
    if state["attempts"] >= state["max_attempts"]:
        return {**state, "status": "done"}
        
    from acrochoreo.llm_client import ask_ai
    verdict = ask_ai(
        f"Target Goal: {state['task']}\n"
        f"Acrobat Output: {state['result']}\n"
        f"Is this routine performance-ready? Answer CONTINUE to retry or STOP if it is perfect."
    )
    
    status = "continue" if "CONTINUE" in verdict.upper() else "done"
    return {**state, "status": status}

# Building the streamlined graph
workflow = StateGraph(TaskState)

workflow.add_node("acrobat", acrobat)
workflow.add_node("choreographer", choreographer)

# Entry point goes straight to the worker for the first attempt
workflow.set_entry_point("acrobat")

# The worker always hands off to the choreographer
workflow.add_edge("acrobat", "choreographer")

# The choreographer decides whether to loop back or terminate
def route_decision(state: TaskState) -> Literal["acrobat", "__end__"]:
    return "acrobat" if state["status"] == "continue" else END

workflow.add_conditional_edges("choreographer", route_decision)

app = workflow.compile()
