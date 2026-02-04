import google.generativeai as genai
import os
from dotenv import load_dotenv

#1 Setup
load_dotenv()
api_key = os.getenv("GEMINI_APO_KEY")
genai.configure(api_key = api_key)
model = genai.GenerativeModel('gemini-2.5-flash')

#2 Load the limited context
def get_document():
    try:
        with open("secret_mission.txt", 'r') as f:
            return f.read()
    except FileNotFoundError:
        return "Error: File not Found."
    
context = get_document

#3 The Anti-Hallucination Function
def ask_the_orcale(question):
    print(f"\n❓ Asking: {question}")
    
    prompt = f"""
    You are a strict Fact-Checking AI.
    Answer the user's question using ONLY the context provided below.
    
    CRITICAL RULES:
    1. If the answer is explicitly written in the context, output the answer.
    2. If the answer is NOT in the context, you MUST say: "I do not have that information."
    3. Do NOT guess. Do NOT use outside knowledge.
    
    CONTEXT:
    {context}
    
    QUESTION:
    {question}
    """
    
    response = model.generate_content(prompt)
    return response.text

# --- THE TEXT ---

#1 Test 1: Something known (Should answer)
print(ask_the_orcale("What is the password?"))

#2 Test 2: Something unknown (Should refuse)
print(ask_the_orcale("What time do we take off?"))

#3 Test 3: Outside knowledge (Should refuse)
# The AI knows what Mars is but it's not in the text
print(ask_the_orcale("Is Mars a planet?"))