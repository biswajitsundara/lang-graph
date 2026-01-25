# %% [0] Import Statements
from typing import TypedDict, Literal
from langgraph.graph import StateGraph, START, END

# %% [1] State Definition
class CreditState(TypedDict):
    age: int
    credit_score: int
    status: str  # To track the final decision

# %% [2] Node Logic
def approval_node(state: CreditState) -> dict:
    return {"status": "✅ Application Approved!"}

def age_rejection_node(state: CreditState) -> dict:
    return {"status": "❌ Rejected: Must be 18 or older."}

def risk_rejection_node(state: CreditState) -> dict:
    return {"status": "❌ Rejected: Credit score too low."}

# %% [3] Router Functions
def route_by_age(state: CreditState) -> Literal["underage", "adult"]:
    if state["age"] < 18:
        return "underage"
    return "adult"

def route_by_credit(state: CreditState) -> Literal["high_risk", "low_risk"]:
    if state["credit_score"] < 650:
        return "high_risk"
    return "low_risk"

# %% [4] Graph Construction
workflow = StateGraph(CreditState)

# Add Nodes
workflow.add_node("approve", approval_node)
workflow.add_node("reject_age", age_rejection_node)
workflow.add_node("reject_risk", risk_rejection_node)

# --- ROUTER 1: Eligibility Check ---
workflow.add_conditional_edges(
    START,
    route_by_age,
    {
        "underage": "reject_age",
        "adult": "check_credit_router" # This is a conceptual jump to the next router
    }
)

# --- ROUTER 2: Risk Check ---
# Note: We can attach a conditional edge to a specific node or a transition point.
# Here, we'll simulate a transition by defining the 'adult' path leads to another check.
workflow.add_conditional_edges(
    "check_credit_router", # This acts as a logic gate
    route_by_credit,
    {
        "high_risk": "reject_risk",
        "low_risk": "approve"
    }
)

# Since "check_credit_router" isn't a physical node, we'll create a simple pass-through node for it
workflow.add_node("check_credit_router", lambda state: state)

# Connect all terminals to END
workflow.add_edge("approve", END)
workflow.add_edge("reject_age", END)
workflow.add_edge("reject_risk", END)

app = workflow.compile()

#%% [5] Visualization
from IPython.display import Image, display
display(Image(app.get_graph().draw_mermaid_png()))

# %% [6] Execution Testing
# Scenario: Adult with bad credit
user_input = {"age": 25, "credit_score": 580, "status": "Pending"}
result = app.invoke(user_input)

print(f"Final Decision: {result['status']}")