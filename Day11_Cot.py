import google.generativeai as genai
import os
from dotenv import load_dotenv

#1 Setup
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key = api_key)
model = genai.GenerativeModel('gemini-2.5-flash')

# A tricky logic question
question = "Roger has 5 tennis balls. He buys 2 more cans of tennis balls. Each can has 3 tennis balls. How much tennis balls does he have now?"

# --- EXPERIMENT 1: The "Fast" Answer ---
print("---🐇 Fast Mode (Direct Question) ---")
response_fast = model.generate_content(question)
print(response_fast.text)

# --- EXPERIMENT 2: Chain of Thought (CoT) ---
print("\n--- 🐢 Reasoning Mode (Chain of Thought) ---")
# The Magic Phrase: "Let's think step by step."
cot_prompt = f"""
Question: {question}

Answer: Let's think step by step.
"""

respones_cot = model.generate_content(cot_prompt)
print(respones_cot.text)