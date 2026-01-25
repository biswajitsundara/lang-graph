from typing import TypedDict
from langgraph.graph import StateGraph, START, END

# [1] State: Tracking our count
class CounterState(TypedDict):
    count: int
    goal: int

# [2] Node: The logic that performs the action
def increment_node(state: CounterState) -> dict:
    print(f"Current count: {state['count']}")
    return {"count": state['count'] + 1}

# [3] Router: The logic that decides whether to loop
def check_goal(state: CounterState) -> str:
    if state['count'] >= state['goal']:
        return "finish"
    return "keep_counting"

# [4] Construction
workflow = StateGraph(CounterState)

workflow.add_node("counter", increment_node)

# Flow: Start -> Node -> Check Goal
workflow.add_edge(START, "counter")

# The Loop: If check_goal returns 'keep_counting', go back to 'counter'
workflow.add_conditional_edges(
    "counter",
    check_goal,
    {
        "keep_counting": "counter",
        "finish": END
    }
)

app = workflow.compile()

# [5] Run it
inputs = {"count": 0, "goal": 3}
result = app.invoke(inputs)

print("-" * 20)
print(f"Final State: {result}")