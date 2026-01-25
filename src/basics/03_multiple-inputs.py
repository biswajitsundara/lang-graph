# %% [1] Imports and State Definition
from typing import TypedDict, List
from langgraph.graph import StateGraph, START, END

class AgentState(TypedDict):
    expenses: List[int]
    user_name: str
    result: str

# %% [2] Logic Node
def calculate_expenses(state: AgentState) -> dict:
    """
    Calculates the sum and returns a partial state update.
    Returning a dict is preferred over mutating the state object directly.
    """
    total = sum(state.get('expenses', []))
    user = state.get('user_name', 'Guest')
    
    # We return only the field we want to update
    return {
        "result": f"Hello {user}, your total expense is ${total:.2f}."
    }

# %% [3] Graph Construction
workflow = StateGraph(AgentState)

# Add the node
workflow.add_node("accountsProcessor", calculate_expenses)

# Define flow: Start -> Processor -> End
workflow.add_edge(START, "accountsProcessor")
workflow.add_edge("accountsProcessor", END)

# Compile
app = workflow.compile()

# %% [4] Visualization
from IPython.display import Image, display
display(Image(app.get_graph().draw_mermaid_png()))


# %% [5] Execution
# Invoke with a dictionary matching our AgentState
input_data = {
    "expenses": [10, 20, 30], 
    "user_name": "Biswa"
}

answers = app.invoke(input_data)

print("-" * 30)
print(answers['result'])
print("-" * 30)
# %%
