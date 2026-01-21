import google.generativeai as genai
import os

# ---------------------------------------------------------
# 1. SETUP: Paste your API key inside the quotes below
# ---------------------------------------------------------
api_key = "HIDDEN_FOR_GITHUB"

# 2. CONFIGURE: Connect to Google
genai.configure(api_key=api_key)

# 3. INITIALIZE: Wake up the model
model = genai.GenerativeModel('gemini-2.5-flash')

# 4. RUN: Ask the AI for a poem
print("... Contacting the AI Brain ...")
response = model.generate_content("Write a short, 2-line poem about a coder named Neha who is learning AI.")

# 5. RESULT: Show the answer
print("\n--- SUCCESS! HERE IS YOUR POEM: ---")
print(response.text)
print("-----------------------------------")