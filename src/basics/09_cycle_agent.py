# %%
from typing import TypedDict
import random
from langgraph.graph import StateGraph, START, END

# %% [1] State Definition
class GameState(TypedDict):
    target: int
    current_guess: int
    attempts: int
    feedback: str

# %% [2] Node Logic
def guesser_node(state: GameState) -> dict:
    """Makes a guess based on previous feedback."""
    attempts = state.get('attempts', 0) + 1
    
    # Simple logic: if no guess, start at 50. 
    # Usually, an LLM would handle the 'strategy' here.
    if state['feedback'] == "Higher":
        new_guess = state['current_guess'] + 5
    elif state['feedback'] == "Lower":
        new_guess = state['current_guess'] - 5
    else:
        new_guess = 50 

    return {
        "current_guess": new_guess,
        "attempts": attempts
    }

def evaluator_node(state: GameState) -> dict:
    """Checks if the guess is correct."""
    guess = state['current_guess']
    target = state['target']
    
    if guess < target:
        fb = "Higher"
    elif guess > target:
        fb = "Lower"
    else:
        fb = "Correct"
        
    return {"feedback": fb}

# %% [3] Loop Router
def should_continue(state: GameState):
    """Router that decides to loop or stop."""
    if state["feedback"] == "Correct":
        return "end"
    return "loop"

# %% [4] Graph Construction
workflow = StateGraph(GameState)

workflow.add_node("guesser", guesser_node)
workflow.add_node("evaluator", evaluator_node)

workflow.add_edge(START, "guesser")
workflow.add_edge("guesser", "evaluator")

# Creating the loop
workflow.add_conditional_edges(
    "evaluator",
    should_continue,
    {
        "loop": "guesser", # This creates the cycle!
        "end": END
    }
)

app = workflow.compile()


#%% [5] Visualization
from IPython.display import Image, display
display(Image(app.get_graph().draw_mermaid_png()))

# %% [6] Execution
input_data = {"target": 95, "current_guess": 0, "attempts": 0, "feedback": ""}
result = app.invoke(input_data)

print(f"Target was {result['target']}. Found in {result['attempts']} attempts!")
# %%
