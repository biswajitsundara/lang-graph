# %%
from typing import TypedDict
from langgraph.graph import StateGraph, START, END

# %% [1] Define the State
class AgentState(TypedDict):
    number1: int
    number2: int
    operation: str
    finalNumber: int   

# %% [2] Define Node Logic
def adder(state: AgentState) -> dict:
    """This node adds two numbers."""
    return {"finalNumber": state['number1'] + state['number2']}

def subtractor(state: AgentState) -> dict:
    """This node subtracts two numbers."""
    return {"finalNumber": state['number1'] - state['number2']}

# %% [3] Define Routing Logic
def decide_next_node(state: AgentState) -> str:
    """Decides which path to take."""
    if state['operation'] == '+':
        return 'addition_path'
    elif state['operation'] == '-':
        return 'subtraction_path'
    else:
        # Better to return a default or error out clearly
        raise ValueError(f"Unknown operation: {state['operation']}")

# %% [4] Construct Graph
workflow = StateGraph(AgentState)

# Add our math nodes
workflow.add_node("add_node", adder)
workflow.add_node("subtract_node", subtractor)

# Use START as the source for the conditional edge to keep it lean
workflow.add_conditional_edges(
    START, 
    decide_next_node, 
    {
        'addition_path': 'add_node',
        'subtraction_path': 'subtract_node'
    }
)

# Connect nodes to END
workflow.add_edge("add_node", END)
workflow.add_edge("subtract_node", END)

# Compile
app = workflow.compile()

# %% [5] Visualization
from IPython.display import Image, display
display(Image(app.get_graph().draw_mermaid_png()))


# %% [6] Execution
# Invoke with a simple dictionary
input_data = {"number1": 10, "number2": 5, "operation": "-"}
result = app.invoke(input_data)

print(f"Operation: {input_data['number1']} {input_data['operation']} {input_data['number2']}")
print(f"Result: {result['finalNumber']}")
# %%
