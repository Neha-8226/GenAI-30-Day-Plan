from google import genai
import os
from dotenv import load_dotenv

# 1. Setup
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# 2. Knowledge Base
documents = [
    "The heavy rain is causing flooding in the streets.", 
    "The stock market crashed due to inflation fears.",   
    "My iPhone battery drains too fast after the update.",
    "The chef prepared a spicy curry with fresh herbs.",  
    "The quarterback threw a touchdown in the final second."
]

# 3. Search Function
def search_knowledge_base(user_query):
    print(f"\n--- 🔎 Searching for: '{user_query}' ---")
    
    prompt = f"""
    You are a Semantic Search Engine.
    Here is the Knowledge Base:
    0: {documents[0]}
    1: {documents[1]}
    2: {documents[2]}
    3: {documents[3]}
    4: {documents[4]}
    
    USER QUERY: "{user_query}"
    
    TASK: Return ONLY the index number (0-4) of the most relevant document.
    """

    try:
        # CHANGED: Using 'gemini-flash-latest' to bypass the 2.0 limit
        response = client.models.generate_content(
            model='gemini-flash-latest', 
            contents=prompt
        )
        best_index = int(response.text.strip())
        print(f"✅ Best Match: \"{documents[best_index]}\"")

    except Exception as e:
        print(f"Error: {e}")

# --- TEST IT (JUST ONE TO BE SAFE) ---
print("--- 🧠 AI Reasoning Search Demo ---")

# We are only running ONE test so we don't trigger the speed limit again!
search_knowledge_base("My device is not working well")

# I have commented out the others for now:
# search_knowledge_base("Is it safe to go outside?")
# search_knowledge_base("Should I save my money?")