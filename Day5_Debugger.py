import google.generativeai as genai
import os
from dotenv import load_dotenv

#1 Setup
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key = api_key)
model = genai.GenerativeModel('gemini-2.5-flash')

#2 Read the broken file
file_path = "broken_script.py"
with open(file_path, "r") as f:
    broken_code = f.read()
    
print(f"--- 🚨 Analyzing {file_path} ---")

#3 The Prompt: "Fix this code"
# We ask for PURE code (no markdown backticks) so we can save it directly.
prompt = f""" 
You are a Senior Python Debugger.
Here is a Python script that contains errors:
{broken_code}

Task: 
1. Identify the bug.
2. Fix the bug (handle the error gracefully or fix the logic).
3. Return ONLY the full, corrected Python code.
4. DO NOT wrap the code in the markdown (no ```python). Just raw code.
"""

#4 Get the fix
response = model.generate_content(prompt)
fixed_code = response.text.strip() # .strip() removes accidental whitespace

print("--- ✅ Bug Fixed! ---")
print("Writing solution to 'fixed_script.py'...")

#5 Save the Fix to a New file
with open ("fixed_script.py", "w") as f:
    f.write(fixed_code)
    
print("Done. Run 'python fixed_script.py' to verify.")