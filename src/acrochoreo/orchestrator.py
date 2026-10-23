from langgraph.graph import StateGraph, END
from typing import TypedDict, Literal

class TaskState(TypedDict):
    task: str
    result: str
    attempts: int
    max_attempts: int
    status: Literal["continue", "done"]

def agent_execution(state: TaskState) -> TaskState:
    """The Acrobat Phase: The agent generates or refines the move sequence."""
    from acrochoreo.llm_client import ask_ai
    
    context = f"Task: {state['task']}"
    if state["result"]:
        context += f"\nYour previous attempt to refine based on your critique: {state['result']}"
        
    result = ask_ai(f"[Acrobat-Choreographer Execution] {context}")
    return {**state, "result": result, "attempts": state["attempts"] + 1}

def agent_critique(state: TaskState) -> TaskState:
    """The Choreographer Phase: The same agent steps back to evaluate its own work."""
    if state["attempts"] >= state["max_attempts"]:
        return {**state, "status": "done"}
        
    from acrochoreo.llm_client import ask_ai
    verdict = ask_ai(
        f"Target Goal: {state['task']}\n"
        f"Your Output: {state['result']}\n"
        f"Critique your own work. Is this performance-ready? Answer CONTINUE to try again or STOP if it is complete."
    )
    
    status = "continue" if "CONTINUE" in verdict.upper() else "done"
    return {**state, "status": status}

# Constructing the Agentic Graph
workflow = StateGraph(TaskState)

# Define the two operational phases of the single agent
workflow.add_node("execution", agent_execution)
workflow.add_node("critique", agent_critique)

# The agent always begins by executing the task
workflow.set_entry_point("execution")

# After executing, the agent automatically shifts to self-critique mode
workflow.add_edge("execution", "critique")

# The agent decides whether to route back into its execution phase or terminate
def route_decision(state: TaskState) -> Literal["execution", "__end__"]:
    return "execution" if state["status"] == "continue" else END

workflow.add_conditional_edges("critique", route_decision)

app = workflow.compile()
