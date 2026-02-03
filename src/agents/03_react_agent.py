## BaseMessage - The foundational class for all message types in LangChain.
## ToolMessage - A message type specifically for tool interactions.
## SystemMessage - A message type for system-level instructions or context.
from json import tool
from typing import TypedDict, Annotated, Sequence
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage, ToolMessage, SystemMessage
from langgraph.graph import StateGraph, START, END
from langchain_cohere import ChatCohere
from langchain_core.tools import Tool
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

load_dotenv()

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]


@tool
def add(a: int, b: int) -> int:
    """Adds two numbers together."""
    return a + b

tools = [add]

llm = ChatCohere(model="command-r-plus-08-2024").bind_tools(tools)

def model_call(state: AgentState) -> AgentState:
    """Process the agent's messages and generate a response."""
    system_prompt =SystemMessage(content="You are a helpful assistant, please answer my question")
    response = llm.invoke(system_prompt + state["messages"])
    return {"messages": [response]}

def should_continue(state: AgentState):
    """Decide whether to continue or stop the agent."""
    messages = state["messages"]
    last_message = messages[-1]
    if not last_message.tool_calls:
        return "end"
    else:
        return "continue"
    
graph = StateGraph(AgentState)
graph.add_node("our_agent", model_call)

tool_node = ToolNode(tools=tools)
graph.add_node("tools", tool_node)
graph.add_edge(START, "our_agent")
graph.add_conditional_edges(
    "our_agent",
    should_continue,
    {"continue": "tools", "end": END}
)
graph.add_edge("tools", "our_agent")

agent = graph.compile()    


def print_stream(stream): 
    for chunk in stream:
        message = chunk["messages"][-1]
        if isinstance(message, Tuple):
            print(message)
        else:
            message.pretty_print()


inputs = {"messages": [("user", "What is 12 plus 30?")]}
print_stream(inputs, stream_mode="values")













