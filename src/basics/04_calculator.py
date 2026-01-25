from typing import TypedDict, List
import math
from langgraph.graph import StateGraph, START, END

# %% [1] Updated State Definition
class AgentState(TypedDict):
    numbers: List[int]
    operation: str  # "+" or "*"
    result: str

# %% [2] Logic Node with Conditional Math
def math_processor(state: AgentState) -> dict:
    nums = state.get('numbers', [])
    op = state.get('operation', '+')
    
    if not nums:
        return {"result": "No numbers provided."}

    if op == '+':
        total = sum(nums)
        op_name = "sum"
    elif op == '*':
        # Multiplies all numbers in the list
        total = math.prod(nums)
        op_name = "product"
    else:
        return {"result": f"Unsupported operation: {op}"}
    
    return {
        "result": f"The {op_name} of {nums} is {total}."
    }

# %% [3] Graph Construction
workflow = StateGraph(AgentState)

# Add the node
workflow.add_node("calculator", math_processor)

# Define flow
workflow.add_edge(START, "calculator")
workflow.add_edge("calculator", END)

# Compile
app = workflow.compile()

# %% [4] Execution (Testing both operations)
print("-" * 30)

# Test Addition
input_add = {"numbers": [10, 20, 30], "operation": "+"}
res_add = app.invoke(input_add)
print(res_add['result'])

# Test Multiplication
input_mult = {"numbers": [2, 5, 10], "operation": "*"}
res_mult = app.invoke(input_mult)
print(res_mult['result'])

print("-" * 30)