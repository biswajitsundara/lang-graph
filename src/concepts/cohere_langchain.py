import os
from dotenv import load_dotenv
from langchain_cohere import ChatCohere
from langchain_core.messages import HumanMessage

# Load API key
load_dotenv()

# Initialize the model
# You can use "command-r-plus" or "command-r"
llm = ChatCohere(
    model="command-r-plus-08-2024", 
    cohere_api_key=os.getenv("COHERE_API_KEY")
)

# Usage
messages = [
    HumanMessage(content="What is the capital of France? give me a short answer.")
]

response = llm.invoke(messages)

print(response.content)