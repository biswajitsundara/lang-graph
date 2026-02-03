from typing import TypedDict, List, Union
from langchain_core.messages import HumanMessage, AIMessage 
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv
from langchain_cohere import ChatCohere 

load_dotenv()

MAX_CONVERSATIONS = 2  # Retain last 5 turns (10 messages)


class AgentState(TypedDict):
    messages: List[Union[HumanMessage | AIMessage]]

llm = ChatCohere(
    model="command-r-plus-08-2024"
)

def process_agent(state:AgentState) -> AgentState:
    """Process the agent's messages and generate a response."""
    max_messages = MAX_CONVERSATIONS * 2
    if len(state["messages"]) > max_messages:
        # Keep only the most recent messages
        state["messages"] = state["messages"][-max_messages:]
        print(f"--- Memory Trimmed: Keeping only last {MAX_CONVERSATIONS} conversations ---")

    response = llm.invoke(state["messages"])
    state["messages"].append(AIMessage(content=response.content))

    print(f"\nAI: {response.content}")

    print("Current State: ", state["messages"])
    return state

graph = StateGraph(AgentState)
graph.add_node("process", process_agent)
graph.add_edge(START, "process")
graph.add_edge("process", END)
agent = graph.compile()

conversation_history = []
user_input = input("Enter: ")

while user_input.lower() not in ["exit", "quit"]:
    conversation_history.append(HumanMessage(content=user_input))
    result = agent.invoke({"messages": conversation_history})
    conversation_history = result["messages"]
    user_input = input("Enter: (or type 'exit' to quit): ")

with open("conversation_history.txt", "w") as file:
    file.write("Your conversation history:\n")
    for message in conversation_history:
        role = "Human" if isinstance(message, HumanMessage) else "AI"
        file.write(f"{role}: {message.content}\n")
    file.write("\nEnd of conversation.\n")

print("Conversation history saved to conversation_history.txt")        