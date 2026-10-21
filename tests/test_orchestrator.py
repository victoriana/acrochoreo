from acrochoreo.orchestrator import TaskState

def test_state_has_required_fields():
    state: TaskState = {
        "task": "test",
        "result": "",
        "attempts": 0,
        "max_attempts": 3,
    }
    assert state["max_attempts"] > 0

def test_route_to_specialist():
    from acrochoreo.orchestrator import route_to_specialist
    state_a: TaskState = {"task": "x", "result": "", "attempts": 0, "max_attempts": 3, "next": "A"}
    state_b: TaskState = {"task": "x", "result": "", "attempts": 0, "max_attempts": 3, "next": "B"}
    assert route_to_specialist(state_a) == "specialist_a"
    assert route_to_specialist(state_b) == "specialist_b"