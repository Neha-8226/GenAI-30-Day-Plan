from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

# 1. Setup
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# 2. The Math Agent Function
def ask_math_agent(question):
    print(f"--- 🧮 Analyzing: {question} ---")
    
    try:
        # FIX: Switched to 'gemini-flash-latest' (Usually has better availability)
        response = client.models.generate_content(
            model='gemini-flash-latest',
            contents=question,
            config=types.GenerateContentConfig(
                tools=[{'code_execution': {}}] 
            )
        )
        
        # 3. Check results
        used_code = False
        
        # We loop through the parts to find the code and the result
        if response.candidates and response.candidates[0].content.parts:
            for part in response.candidates[0].content.parts:
                if part.executable_code:
                    print(f"\n[🤖 WROTE CODE]:\n{part.executable_code.code}")
                    used_code = True
                if part.code_execution_result:
                    print(f"\n[⚡ EXECUTED RESULT]:\n{part.code_execution_result.output}")

        if not used_code:
            print("\n[NOTE]: The model answered from memory (didn't use code).")

        return response.text

    except Exception as e:
        return f"Error: {e}"

# --- TEST IT ---
user_query = input("Ask a math/logic question (e.g., 'Sum of first 50 prime numbers'): ")
answer = ask_math_agent(user_query)

print("\n--- 📝 Final Answer ---")
print(answer)