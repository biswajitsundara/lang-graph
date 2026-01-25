# %%
from typing import TypedDict, List
from langgraph.graph import StateGraph, START, END

# %%
class AgentState(TypedDict):
    name: str
    age: str
    final: str

# %%
def first_node(state: AgentState) -> dict:
    # Instead of mutating state['final'], we return a partial update
    return {"final": f"Hello, {state['name']}"}

# %%
def second_node(state: AgentState) -> dict:
    # We access the existing 'final' from the state and update it
    updated_text = state['final'] + f" you are {state['age']} years old"
    return {"final": updated_text}

# %%
workflow = StateGraph(AgentState)
workflow.add_node("first_node", first_node)
workflow.add_node("second_node", second_node)

workflow.add_edge(START, "first_node")
workflow.add_edge("first_node", "second_node")
workflow.add_edge("second_node", END)

app = workflow.compile()

# %%
from IPython.display import Image, display
display(Image(app.get_graph().draw_mermaid_png()))


# %%
result = app.invoke({"name": "Alice", "age": "30"})
print(result['final'])
# %%
