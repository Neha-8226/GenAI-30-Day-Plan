import google.generativeai as genai
import os
from dotenv import load_dotenv

#1 Setup
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key = api_key)
model = genai.GenerativeModel('gemini-2.5-flash')

#2 The Retrieval Function (The "Reader")
def get_document_context(filename):
    try:
        with open(filename, 'r') as f:
            return f.read()
    except FileNotFoundError:
        return "Error: File not found."
    
#3 The RAG Generation Function (The "Thinker")
def ask_document(question, context_text):
    print("\n---🤖 Reading Document & Thinking... ---")
    
    # This is the RAG Magic: We paste the document INTO the promot
    prompt = f"""
    You are a Helpful Assistant. Answer the user's question ONLY based on the context provided below.
    If the answer is not in the text, say "I don't know."
    
    CONTEXT:
    {context_text}
    
    USER QUESTION:
    {question}
    """
    
    response = model.generate_content(prompt)
    return response.text

# --- MAINEXECUTION ---
# Load the secret file
document_content = get_document_context("secret_mission.txt")

print("--- 📝 Document Loaded: secret_mission.txt ---")
user_query = input("Ask a question about the mission: ")

# Run the RAG pipeline
answer = ask_document(user_query, document_content)

print(f"\n[ANSWER]: {answer}")