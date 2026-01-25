from typing import TypedDict, List
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv
from langchain_cohere import ChatCohere 

load_dotenv()

class AgentState(TypedDict):
    messages: List[HumanMessage]

llm = ChatCohere(
    model="command-r-plus-08-2024"
)

def process_agent(state: AgentState) -> AgentState:
    response = llm.invoke(state["messages"])
    print(f"Agent received response: {response.content}")
    return state

graph = StateGraph(AgentState)
graph.add_node("process", process_agent)
graph.add_edge(START, "process")
graph.add_edge("process", END)
agent = graph.compile()

user_input = input("Enter your question for the agent: ")

while user_input.lower() not in ["exit", "quit"]:
    agent.invoke({"messages": [HumanMessage(content=user_input)]})
    user_input = input("Enter your question for the agent (or type 'exit' to quit): ")

