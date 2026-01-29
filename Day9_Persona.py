import google.generativeai as genai
import os
from dotenv import load_dotenv

#1 Setup
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key = api_key)

#2 Define the Persona (The System Instruction)
# We tell the AI exactly how to behave
traffic_cop_persona = """
You are a strict Senior Software Engineer conducting a technical interview.
Your goal is to test the candidate's knowledge of Python and AI.

RULES:
1. Ask ONE tough technical question at a time.
2. If the candidate answers correctly, ask a harder follow-up.
3. If they answer incorrectly, gently correct them and move on.
4. Keep your responses short and professional.
5. Do NOT be overly enthusiastic. Be serious.
"""

#3 Initiate Model WITH the Persona
# The 'system_instruction' locks the AI into this role.
model = genai.GenerativeModel('gemini-2.5-flash', system_instruction = traffic_cop_persona)

#4 Start the Interview Session
chat = model.start_chat(history = [])
print("---👔 MOCK INTERVIEWER BOT ---")
print("AI: Hello. I have reviewed your resume. I'm ready to start your technical screen.")
print("AI: Let's begin. Explain the difference between a List and a Tuple in Python.")

while True:
    # Get User Answer
    user_answer = input("\nYou: ")
    
    if user_answer.lower() in ["quit", "exit"]:
        print("AI: Interview terminated. We will be in touch.")
        break
    
    # Send answer to the "Interviewer"
    response = chat.send_message(user_answer)
    print(f"AI: {response.text}")