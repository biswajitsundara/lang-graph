# %% [1] Setup and Imports
from typing import TypedDict
from langgraph.graph import StateGraph, START, END

# Define the shape of our state
class AgentState(TypedDict):
    name: str
    greeting: str

# %% [2] Define the Compliment Logic
def compliment_node(state: AgentState) -> AgentState:
    """Takes the name and generates a personalized compliment."""
    
    ## user_name = state["name"] 
    # Result: ❌ KeyError if "name" is missing
    # This is safe access with a default value
    user_name = state.get("name", "Friend")

    compliment = f"{user_name} you are doing amazing job"
    
    # We return the update for the 'greeting' key
    return {"greeting": compliment}

# %% [3] Build the Graph
workflow = StateGraph(AgentState)

# Add our node
workflow.add_node("complimenter", compliment_node)

# Define the simplest possible path
workflow.add_edge(START, "complimenter")
workflow.add_edge("complimenter", END)

# Compile the graph into an executable app
app = workflow.compile()

# %% [4] Run the Agent
# Input: passing the name 'Bob'
initial_input = {"name": "Alia"}
result = app.invoke(initial_input)

# Output the result
print("-" * 30)
print(result["greeting"])
print("-" * 30)