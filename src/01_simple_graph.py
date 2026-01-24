# %% [1] Imports and State
from typing import TypedDict
from langgraph.graph import StateGraph

class AgentState(TypedDict):
    message: str

# %% [2] Define the Node
def greeting_node(state: AgentState) -> AgentState:
    """Simple node that adds a message to the state"""
    state['message'] = "Hey " + state['message'] + ", how is your day going?"
    return state

# %% [3] Build and Compile
workflow = StateGraph(AgentState)
workflow.add_node('greeter', greeting_node)
workflow.set_entry_point('greeter')
workflow.set_finish_point('greeter')
app = workflow.compile()

# %% [4] Visualize the Graph (mermaid)
from IPython.display import Image, display  # <--- Add this line!
display(Image(app.get_graph().draw_mermaid_png()))

# %% [5] Run the Graph
initial_input = {"message": "Kareena"}
result = app.invoke(initial_input)
print(result['message'])
# %%
