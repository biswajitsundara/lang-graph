import os
import cohere
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()
api_key = os.getenv("COHERE_API_KEY")

# Initialize client (using V2 for the latest features)
co = cohere.ClientV2(api_key)

def list_my_models():

    try: 
        # Fetch models compatible with the 'chat' endpoint
        response = co.models.list(endpoint="chat")

        model_count = len(response.models)
        print("✅ Success! Your API key is valid and working.")
        print(f"You have access to {model_count} models.")
    
        print("--- Available Chat Models ---")
        for model in response.models:
            print(f"Model Name: {model.name}")
            print(f"Context Length: {model.context_length}")
            print("-" * 30)
    except Exception as e:
        # This will catch 401 Unauthorized or other connection issues
        print(f"❌ Connection failed.")
        print(f"Error accessing Cohere API: {e}")        

list_my_models()


def get_cohere_response(prompt):
    # 'command-r-plus' or 'command-r' are standard high-performance choices
    response = co.chat(
        model="command-r-plus-08-2024",
        messages=[
            {
                "role": "user", 
                "content": prompt
            }
        ]
    )
    
    # Accessing the text content in V2
    return response.message.content[0].text

# Usage
answer = get_cohere_response("What is the capital of France?")
print(f"Cohere says: {answer}")