"""
Lang chain core concepts
StateGraph, nodes, edges, and basic patterns
"""
from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph, START, END
from typing_extensions import Annotated, TypedDict
from langchain_core.messages import BaseMessage, ChatMessage, SystemMessage, HumanMessage, AIMessage
import operator
from utils.visualize_graph import visualize_and_display_graph  
from dotenv import load_dotenv  

load_dotenv()  # Load environment variables from .env file

## -----------------------------------------
# 0. HELLO WORLD GRAPH
# -----------------------------------------


def demo_hello_world_graph():
    # 1. Define your Graph State (memory structure)
    class State(TypedDict):
        message: str

    # 2. Define a simple Node (a function that modifies state)
    def hello_world_node(state: State) -> dict:
        return {"message": f"Hello {state['message']}"}

    # 3. Build the Graph
    graph = StateGraph(State)

    # Add the node and define entry/exit flow
    graph.add_node("hello_node", hello_world_node)
    graph.add_edge(START, "hello_node")
    graph.add_edge("hello_node", END)

    # 4. Compile the Graph into an executable application
    app = graph.compile()

    visualize_and_display_graph(app, filename="graph0.png")   

    result = app.invoke({"message": "Alia"})
    print(result["message"])


## -----------------------------------------
# 1. SIMPLE GRAPH EXAMPLE
## -----------------------------------------

# --- STEP 1: DEFINE GRAPH STATE ---
# The State object acts as shared memory accessible to every node.
# Every node reads from this dictionary and returns key updates to it.
class SimpleState(TypedDict):
    """A simple state representation for the graph."""
    input: str
    output: str
    step: int


def demo_simple_graph():
    
    # --- STEP 2: DEFINE GRAPH NODES ---
    # A Node is just a standard Python function that takes the state,
    # processes it, and returns a dictionary with key updates.
    def process(state: SimpleState) -> dict:
        """A simple processing function that transforms the state."""
        return {
            "output": state["input"].upper(),
            "step": state["step"] + 1
        }
    
    # --- STEP 3: CONSTRUCT THE GRAPH ---
    # Instantiate the StateGraph with our state schema
    graph = StateGraph(SimpleState)

    # Register the node under the name 'process'
    graph.add_node("process", process)

    # Define directional edges to guide execution flow
    graph.add_edge(START, "process") # Flow starts and immediately goes to 'process'
    graph.add_edge("process", END) # After 'process' finishes, terminate execution

    # --- STEP 4: COMPILE THE GRAPH ---
    # Compile turns your graph structure into an executable runnable application
    app = graph.compile()


    # --- STEP 5: Visualize the Graph (optional) ---
    visualize_and_display_graph(app, filename="graph1.png")   


    # --- STEP 6: EXECUTE THE GRAPH ---
    # Pass the initial state using .invoke() to trigger execution
    result = app.invoke({"input": "hello", "output": "", "step": 0})

    #Output result to verify the transformations
    print(f"input: {result['input']}, output: {result['output']}, step: {result['step']}")  

    # The output will be
    # input: hello, output: HELLO, step: 1


## -----------------------------------------
# 2. USING REDUCER AND ACCUMULATING STATE
## -----------------------------------------

# --- STEP 1: DEFINE REDUCER-ENABLED STATE ---
class AccumulatingState(TypedDict):
    """A state representation that accumulates outputs."""
    # Reducer 1: operator.add on lists performs list concatenation ([old] + [new]
    messages: Annotated[list[str], operator.add]
    # Reducer 2: operator.add on integers performs numeric addition (old + new)
    count: Annotated[int, operator.add]

def demo_accumulating_graph():
    # --- STEP 2: DEFINE GRAPH NODES ---
    # Nodes do not need to read or calculate the total existing state;
    # they only return the partial update. The reducers handle the merging logic.
    def step_one(state: AccumulatingState) -> dict:
        """First step that adds a message and increments count."""
        return {
            "messages": ["Step 1 executed"],
            "count": 1
        }
    
    def step_two(state: AccumulatingState) -> dict:
        """Second step that adds another message and increments count."""
        return {
            "messages": ["Step 2 executed"],
            "count": 1
        }

    # --- STEP 3: CONSTRUCT THE GRAPH ---
    graph = StateGraph(AccumulatingState)
    graph.add_node("step_one", step_one)
    graph.add_node("step_two", step_two)

    # Define simple sequential execution flow
    graph.add_edge(START, "step_one")
    graph.add_edge("step_one", "step_two")
    graph.add_edge("step_two", END)

    # --- STEP 4: COMPILE AND EXECUTE ---
    app = graph.compile()


    visualize_and_display_graph(app, filename="graph2.png")   

    print("Graph saved as graph.png") 

    # Initial state passed in:
    # messages = ["Initial message"], count = 0
    result = app.invoke({"messages": ["Initial message"], "count": 0})

    # Output the final accumulated values
    print("Accumulated messages:", result["messages"])
    print("Total count:", result["count"])


#---------------------------------------------------------
# MESSAGE STATE GRAPH EXAMPLE
#---------------------------------------------------------

# from langgraph.graph import add_messages

class MessageState(TypedDict):
    """A state representation for accumulating chat messages."""
    messages: Annotated[list[BaseMessage], operator.add]

def demo_message_state():
    llm = init_chat_model(model="command-r-plus-08-2024", temperature=0)

    def chat_node(state: MessageState) -> dict:
        """A node that adds a system message to the state."""
        response = llm.invoke(state["messages"])
        return {"messages": [response]}
    
    graph = StateGraph(MessageState)
    graph.add_node("chat_node", chat_node)
    graph.add_edge(START, "chat_node")
    graph.add_edge("chat_node", END)

    app = graph.compile()
    result = app.invoke({"messages": [HumanMessage(content="Say hello in French")]})
    print("Chat response:")
    for msg in result["messages"]:
        role = "Human" if isinstance(msg, HumanMessage) else "AI"
        print(f"{role}: {msg.content}")


if __name__ == "__main__":
    #demo_hello_world_graph()
    #demo_simple_graph()
    #demo_accumulating_graph()
    demo_message_state()