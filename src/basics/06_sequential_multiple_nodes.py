# %% [1] Imports and State Definition
from typing import TypedDict, List, Annotated
import operator
from langgraph.graph import StateGraph, START, END

class AgentState(TypedDict):
    name: str
    age: str
    # The operator.add tells LangGraph to append to this list 
    # rather than replacing it when a node returns a value.
    skills: Annotated[List[str], operator.add]
    final: str

# %% [2] Node Logic
def name_node(state: AgentState) -> dict:
    return {"final": f"Hello, {state['name']}"}

def age_node(state: AgentState) -> dict:
    updated_text = state['final'] + f" (Age: {state['age']})"
    return {"final": updated_text}

def skill_node(state: AgentState) -> dict:
    """Adds specific skills to the state."""
    new_skills = ["Python", "Machine Learning", "LangGraph"]
    
    # We don't need to manually append; the Annotated list handles it!
    return {
        "skills": new_skills,
        "final": state['final'] + f" is skilled in: {', '.join(new_skills)}."
    }

# %% [3] Graph Construction
workflow = StateGraph(AgentState)

workflow.add_node("name_node", name_node)
workflow.add_node("age_node", age_node)
workflow.add_node("skill_node", skill_node)

# Flow: Start -> Name -> Age -> Skills -> End
workflow.add_edge(START, "name_node")
workflow.add_edge("name_node", "age_node")
workflow.add_edge("age_node", "skill_node")
workflow.add_edge("skill_node", END)

app = workflow.compile()

# %% [4] Execution
input_data = {
    "name": "Alice", 
    "age": "30",
    "skills": ["Communication"] # Initial skill
}

result = app.invoke(input_data)

print("--- FINAL RESULT ---")
print(f"Message: {result['final']}")
print(f"Full Skill List: {result['skills']}")
# %%
