import os
from typing import TypedDict, Annotated, Sequence
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage, ToolMessage, SystemMessage, HumanMessage
from langgraph.graph import StateGraph, START, END
from langchain_cohere import ChatCohere
from langchain_core.tools import tool
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

load_dotenv()

# Global variable for demo purposes
document_content = ""

class AgentState(TypedDict):
    # add_messages ensures new messages are appended to the history
    messages: Annotated[Sequence[BaseMessage], add_messages]

@tool
def update_document(content: str) -> str:
    """Updates the document with the provided content."""
    global document_content
    document_content = content
    return f"Document updated. Current content is: {document_content}"

@tool
def save_document(filename: str) -> str:
    """Saves the current document content to a text file."""
    global document_content
    if not filename.endswith(".txt"):
        filename = f"{filename}.txt"
    try:
        with open(filename, "w") as f:
            f.write(document_content)
        return f"Document saved as {filename}."
    except Exception as e:
        return f"Failed to save document: {str(e)}"

tools = [update_document, save_document]
# Use a high-quality model for tool calling
model = ChatCohere(model="command-r-plus-08-2024").bind_tools(tools)

def our_agent(state: AgentState):
    system_prompt = SystemMessage(content=f"""
        You are a drafting assistant. 
        - To update a draft, use 'update_document'.
        - To save, use 'save_document'.
        - Current draft state: {document_content}
        After updating, ask the user if they are happy or need changes.
    """)
    
    # We pass the full history to the model
    messages = [system_prompt] + state["messages"]
    response = model.invoke(messages)
    return {"messages": [response]}

def should_continue(state: AgentState) -> str:
    """Determine if we should route to tools or finish."""
    last_message = state["messages"][-1]
    
    # If the LLM makes tool calls, we must go to the "tools" node
    if last_message.tool_calls:
        return "tools"
    
    # Otherwise, we check if the task is complete (e.g., document saved)
    # We look back to see if the last tool output confirmed a save
    for message in reversed(state["messages"]):
        if isinstance(message, ToolMessage):
            if "saved" in message.content.lower():
                return "end"
            break # Only check the most recent tool result
            
    return "end"
       

def print_messages(messages):
    """Function I made to print the messages in a more readable format"""
    if not messages:
        return
    
    for message in messages[-3:]:
        if isinstance(message, ToolMessage):
            print(f"\n🛠️ TOOL RESULT: {message.content}")


# Graph Construction
workflow = StateGraph(AgentState)

workflow.add_node("agent", our_agent)
workflow.add_node("tools", ToolNode(tools))

workflow.add_edge(START, "agent")

# Updated mapping to match the return values of should_continue
workflow.add_conditional_edges(
    "agent", 
    should_continue, 
    {
        "tools": "tools", 
        "end": END
    }
)

workflow.add_edge("tools", "agent")

app = workflow.compile()


def run_document_agent():
    print("\n ===== DRAFTER (Type 'quit' to exit) =====")
    
    # Initialize state
    state = {"messages": []}
    
    while True:
        user_input = input("\nUser: ")
        if user_input.lower() in ["quit", "exit", "q"]:
            break

        # Add the new message to the state
        state["messages"].append(HumanMessage(content=user_input))
        
        # Stream the graph execution
        # We use the updated state from the previous loop iteration
        for step in app.stream(state, stream_mode="values"):
            state = step # Update local state with graph results
            if "messages" in step:
                print_messages(step["messages"])
        
        # Check if the graph decided to END based on your should_continue logic
        # We look at the last message to see if the LLM is done
        last_msg = state["messages"][-1]
        if not last_msg.tool_calls and "saved" in str(last_msg).lower():
            print("\nSystem: Document process complete.")
            break

    print("\n ===== DRAFTER FINISHED =====")

if __name__ == "__main__":
    run_document_agent()