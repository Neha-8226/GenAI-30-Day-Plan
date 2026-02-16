import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

#1 Setup
load_dotenv()
client = genai.Client(api_key = os.getenv("GEMINI_API_KEY"))

# --- 2 Tools ---

def search_internal_database(query: str) -> str:
    """Use this tool ONLY to search for internal company secrets, policies, or passwords."""
    print(f"\n 🔎 [AGENT DECISION: Searching Internal DB for '{query}']")
    
    # In a real app, this is where your Day 22 PureVectorDB code goes
    # For this script, we use a simple mock dictionary to prove thr routing works
    mock_db = {
        "password": "The secret company Wi-Fi password is 'BlueBanana2026'.",
        "pto": "Employees get 20 days of Paid Time Off (PTO) per year."
    }
    
    for key, value in mock_db.items():
        if key in query.lower():
            return value
    return "No internal document found."

def get_public_weather(location: str) -> str:
    """Use this tool ONlY to get the current weather for a specific city."""
    print(f"\n ☁️ [AGENT DECISION: Fetching Weather API for '{location}']")
    
    # In a real app, this would call a real weather API
    return f"The weather in {location} is currently 72°F and sunny."

# --- 3 THE AGENT SETUP ---

# We give the LLM a list of functions it is allowed to use.
my_tools = [search_internal_database, get_public_weather]

# We use the Chat interface so it can automatically call the tools
agent_chat = client.chats.create(
    model = "gemini-2.5-flash",  # Using the latest model
    config = types.GenerateContentConfig(
        tools = my_tools,
        temperature = 0.1 # Keep it low so it thinks logically
    )
)

print("---🤖 Agentic RAG Initialized ---")
print("I am an autonomous agent. I can search internal docs or check external APIs.")

# ---4 THE TEST RUN ---
# We will ask it three completely different questions to test its routing logic

questions = [
    "What is the company Wi-Fi password?", # Should trigger internal database
    "What is the weather like in Pune?", # Should trigger external weather API
    "What is the capital of France?"  # Should use general knowledge (no tools)
]

for q in questions:
    print(f"\n🗣️ User: {q}")
    # The SDK automatically handles the background tool calling loop here!
    response = agent_chat.send_message(q)
    print(f"🤖 Agent: {response.text}")