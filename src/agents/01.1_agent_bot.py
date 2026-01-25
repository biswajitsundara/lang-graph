from typing import TypedDict, Annotated, Sequence
from operator import add
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv
from langchain_cohere import ChatCohere 

load_dotenv()

# 1. Use Annotated and add (reducer) to keep a running history
class AgentState(TypedDict):
    # BaseMessage covers Human, AI, and System messages
    messages: Annotated[Sequence[BaseMessage], add]

llm = ChatCohere(model="command-r-plus-08-2024")

def process_agent(state: AgentState):
    # Invoke the LLM with the full history
    response = llm.invoke(state["messages"])
    
    # Return the AI message to APPEND it to the state via the reducer
    return {"messages": [response]}

# 2. Build the Graph
workflow = StateGraph(AgentState)
workflow.add_node("process", process_agent)
workflow.add_edge(START, "process")
workflow.add_edge("process", END)

# Compile
agent = workflow.compile()

# 3. Interactive Loop with Memory
print("Type 'exit' to quit.")
# Keep track of the session history outside the loop or use a Checkpointer
current_messages = []

while True:
    user_input = input("\nUser: ")
    if user_input.lower() in ["exit", "quit"]:
        break
    
    current_messages.append(HumanMessage(content=user_input))
    
    # Run the agent
    result = agent.invoke({"messages": current_messages})
    
    # Update our local list with the full state (which now includes AI's response)
    current_messages = result["messages"]
    
    # Print only the last message (the AI's response)
    print(f"AI: {current_messages[-1].content}")