## Reducer Function: A function that takes a list of items and reduces them to a single item, 
# like summing numbers or concatenating strings.
# Reducer function controls how updates from multiple nodes are combined into one (existing state)
# Tells us how to merge new information into existing state in the graph.
# Without a reducer updates would overwrite existing state instead of merging.

## Example: 
# state = {"messages": ["Hi"]}
# updates = {"messages": ["Hello"]}
# with reducer that appends messages, final state = {"messages": ["Hi", "Hello"]}
# without reducer, final state = {"messages": ["Hello"]}

## The reducer function works this way
# The worker (merge_logic) - first argument - is the function that defines how to merge two items
# The raw data (updates) - second argument - is the list of updates to be merged
# The initial state (state) - third argument - is the starting point for the reduction

# add_messages is a built-in reducer that appends lists together in lang graph


from functools import reduce

# 1. You MUST define a function to do the merging
def merge_logic(current_state, update):
    return {"messages": current_state["messages"] + update["messages"]}

state = {"messages": ["Hi"]}
updates = [
    {"messages": ["Hello"]},
    {"messages": ["How are you?"]},
    {"messages": ["I am fine!"]}
]

# 2. Correct Order: (Function, Data_List, Initial_State)
final_state = reduce(merge_logic, updates, state)

print(final_state)
# Output: {'messages': ['Hi', 'Hello', 'How are you?', 'I am fine!']}