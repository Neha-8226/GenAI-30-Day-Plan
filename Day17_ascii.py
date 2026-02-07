from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

# 1. Setup
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# 2. Read the Local Data
try:
    with open("sales_data.csv", "r") as f:
        csv_content = f.read()
    print("--- 📂 Loaded sales_data.csv ---")
except FileNotFoundError:
    print("Error: Create 'sales_data.csv' first!")
    exit()

# 3. The Analyst Function
def analyze_data_text(data_string, prompt):
    print(f"--- 📊 Analyst Working on: {prompt} ---")
    
    # We ask for a TEXT-BASED chart. This bypasses the file transfer bug.
    full_prompt = f"""
    Here is a CSV dataset:
    {data_string}
    
    Task: {prompt}
    
    IMPORTANT: 
    1. Write a Python script to analyze the numbers.
    2. PRINT a text-based bar chart using symbols (like '#' or '*').
    3. PRINT a short "Executive Summary" of the trends.
    4. Do NOT use matplotlib. Do NOT save files. Just print to console.
    """

    try:
        response = client.models.generate_content(
            model='gemini-flash-latest',
            contents=full_prompt,
            config=types.GenerateContentConfig(
                tools=[{'code_execution': {}}] 
            )
        )
        
        # 4. Show the Output
        if response.candidates and response.candidates[0].content.parts:
            for part in response.candidates[0].content.parts:
                if part.executable_code:
                    print(f"\n[🤖 LOGIC]:\n{part.executable_code.code}")
                if part.code_execution_result:
                    print(f"\n[⚡ REPORT DASHBOARD]:\n{part.code_execution_result.output}")
        
        return "Analysis Complete."

    except Exception as e:
        return f"Error: {e}"

# --- TEST IT ---
user_request = "Visualize the Sales trends and calculate the profit margin."
result = analyze_data_text(csv_content, user_request)