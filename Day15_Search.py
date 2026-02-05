from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

#1 Setup
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key = api_key)

#2 The Search Foundation
def ask_google(query):
    print(f"---🌎 Searching Google for: {query} ---")
    
    try:
        # Using the standard Gemini 2.0 Flash model with new key
        response = client.models.generate_content(model = 'gemini-2.0-flash', 
                                                  contents = query, 
                                                  config = types.GenerateContentConfig(
                                                      tools = [types.Tool(
                                                          google_search = types.GoogleSearch()
                                                      )]
                                                  )
                                                 )
        #3 Print Source
        if response.candidates[0].grounding_metadata.search_entry_point:
            print("\n[SOURCE]: Found Google search results.")
            return response.text
    except Exception as e:
        return f"Error: {e}"
    
# --- TEST IT ---
user_query = input("Ask a real-time question: ")
answer = ask_google(user_query)

print("\n--- 🤖 AI Answer ---")
print(answer)