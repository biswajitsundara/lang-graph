```python
## Install Langgraph
%pip install -U langgraph
```

   
### Phase 1: Preparation
```python
from typing import Dict, TypedDict
from langgraph.graph import StateGraph
```
* `TypedDict:` A special Python dictionary that allows us to define the "schema" (the keys and data types) that our graph will use.

* `StateGraph:` The main class used to build the workflow. It acts like a construction kit for the logic.


### Phase 2: Defining the "Memory"
```python
# Define the State (Data structure only)
class AgentState(TypedDict):
    message: str
```
* This defines the State. Think of this as a shared "notebook" that every part of your program can read from and write to.
* Here, we are telling LangGraph: "Every time you run, you must have a key called message which is a string."


### Phase 3: The "Worker" (Node)
```python
# Define the Node (A standalone function)
def greeting_node(state: AgentState) -> AgentState:
    """Simple node that adds a message to the state"""
    state['message'] = "Hey " + state['message'] + ", how is your day going?"
    return state
```
* `greeting_node:` This is a function that acts as a Node (a step in your process).

* `(state: AgentState):` It takes the current state (the notebook) as input.

* `state['message']` = ...: It performs a task—in this case, simple string manipulation.

* `return state:` It passes the updated notebook back to the graph.


### Phase 4: Building the Map (Graph)
```python
# Initializes the graph and tells it to follow the structure defined in AgentState.
graph = StateGraph(AgentState)

# Registers the function. We name this step 'greeter' so the graph can reference it later.
graph.add_node('greeter', greeting_node)

# Tells the graph: "When you start, go straight to the 'greeter' node."
graph.set_entry_point('greeter')

# Tells the graph: "Once 'greeter' is finished, the entire process is complete."
graph.set_finish_point('greeter')

# This "bakes" the graph. It validates that your entry and exit points are valid and turns the blueprint into a runnable application.
app = graph.compile()
```

### Phase 5: Visualization & Execution
```python
from IPython.display import Image, display
display(Image(app.get_graph().draw_mermaid_png()))
```
draw_mermaid_png(): Generates a visual flow chart of your logic. In this specific code, the chart shows a direct line from Start -> Greeter -> End.



### Phase 6: Execution
```python
result = app.invoke({"message": "Biswa"})
```
* `invoke:` This triggers the graph. We provide the starting state where message is "Biswa".
* The graph starts at the entry point, runs greeting_node, and then stops.

### Phase 7: Result
```python
result['message']
```
* The result is the final version of the State notebook after all nodes have finished their work.

```console
'Hey Biswa, how is your day going?'
```
