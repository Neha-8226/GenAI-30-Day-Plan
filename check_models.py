import google.generativeai as genai
import os
from dotenv import load_dotenv

#1 Setup
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key = api_key)

print("--- Checking available models for your library ---")

#2 List all models available to your API key
try:
    for m in genai.list_models():
        # We only care about models that can generate text
        if 'generateContent' in m.supported_generation_methods:
            print(f"Found: {m.name}")
except Exception as e:
    print(f"Error listing models: {e}")