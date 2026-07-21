"""
Lang chain core concepts
StateGraph, nodes, edges, and basic patterns
"""
from colorama import init
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


#---------------------------------------------------------
# MULTI STEP MESSAGE STATE GRAPH EXAMPLE
#---------------------------------------------------------
class MultiStepState(TypedDict):
    input: str
    analyzed: str
    enhanced: str
    final: str

def demo_multi_step_message_state():
    llm = init_chat_model(model="command-r-plus-08-2024", temperature=0)

    def analyze_node(state: MultiStepState) -> dict:
        """Analyze the input and produce an analysis."""
        analysis = llm.invoke([HumanMessage(content=f"Analyze this and generate response in one sentence: {state['input']}")])
        return {"analyzed": analysis.content}

    def enhance_node(state: MultiStepState) -> dict:
        """Enhance the analyzed content."""
        enhancement = llm.invoke([HumanMessage(content=f"Take the following text and enhance it with more details in two sentences: {state['analyzed']}")])
        return {"enhanced": enhancement.content}

    def finalize_node(state: MultiStepState) -> dict:
        """Finalize the enhanced content."""
        finalization = llm.invoke([HumanMessage(content=f"Take the following text and finalize it in one sentence concise summary: {state['enhanced']}")])
        return {"final": finalization.content}

    graph = StateGraph(MultiStepState)
    graph.add_node("analyze_node", analyze_node)
    graph.add_node("enhance_node", enhance_node)
    graph.add_node("finalize_node", finalize_node)

    graph.add_edge(START, "analyze_node")
    graph.add_edge("analyze_node", "enhance_node")
    graph.add_edge("enhance_node", "finalize_node")
    graph.add_edge("finalize_node", END)

    app = graph.compile()
    result = app.invoke({"input": "Artificial Intelligence"})
    
    print("Input:", result["input"])
    print("Analyzed:", result["analyzed"][:100])  # Print first 100 characters of analyzed content
    print("Enhanced:", result["enhanced"][:100])      
    print("Final output:", result["final"])


#---------------------------------------------------------
# EXERCISE: CREATE A LANG GRAPH THAT GENERATES QUESTIONS AND ANSWERS
#---------------------------------------------------------

def exercise_first_lang_graph():
    """
    Create a lang graph that:
    - Takes a topic as input
    - Node 1: Generates 3 questions about the topic
    - Node 2: Answers one of the questions
    - Returns both question and answer
    """

    class QAState(TypedDict):
        topic: str
        question: str
        answer: str

    llm = init_chat_model(model="command-r-plus-08-2024", temperature=0)

    def generate_questions(state: QAState) -> dict:
        response = llm.invoke(
            f"Generate 3 interesting questions about: {state['topic']}\n"
            "Format: numbered list"
        )
        return {"question": response.content}
    
    def answer_question(state: QAState) -> dict:
        response = llm.invoke(
            f"Pick ONE question from the following list and provide a detailed answer:\n\n{state['question']}"
        )
        return {"answer": response.content}
    
    graph = StateGraph(QAState)
    graph.add_node("generate_questions", generate_questions)
    graph.add_node("answer_question", answer_question)

    graph.add_edge(START, "generate_questions")
    graph.add_edge("generate_questions", "answer_question")
    graph.add_edge("answer_question", END)

    app = graph.compile()
    result = app.invoke({"topic": "The future of renewable energy"})

    print("\nExercise result:")
    print(f"Topic: {result['topic']}\n")
    print(f"Questions Generated:\n{result['question']}\n")  # Fixed key here
    print(f"Answer Selected:\n{result['answer']}")


if __name__ == "__main__":
    #demo_hello_world_graph()
    #demo_simple_graph()
    #demo_accumulating_graph()
    #demo_message_state()
    #demo_multi_step_message_state()
    exercise_first_lang_graph()