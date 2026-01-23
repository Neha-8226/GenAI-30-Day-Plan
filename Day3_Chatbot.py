import google.generativeai as genai
import os
from dotenv import load_dotenv

#1 Load the secret key(Security First)
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

#2 Initialize the Model
model = genai.GenerativeModel('gemini-2.5-flash')

#3 Start the Chat Session (This creates the "Memory")
# history = [] starts us with a blank slate 
chat = model.start_chat(history=[])

#4 The system context (We send this first, silently)
initial_prompt = "You are a friendly but strict technical interviewer. Ask the user their name, then ask them one technical question about Python. Wait for their answer, then grade it."
chat.send_message(initial_prompt)

print("---🤖 AI INTERVIEWER BOT (Type 'quit' to exit) ---")
print("AI: Hello! I am your interviewer today. Let's start.")

#5 The Conversation Loop
while True:
    # Get User Input
    user_input = input("\nYou: ")
    
    # Exit Condition
    if user_input.lower() in ["quit", "exit", "bye"]:
        print("AI: Good luck with your interview process!")
        break
    
    # Send message to AI and get response
    # (The 'chat' object automatically remembers the previous turns)
    response = chat.send_message(user_input)
    
    # Print AI Response
    print(f"AI: {response.text}")