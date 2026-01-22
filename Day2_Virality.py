import google.generativeai as genai
import os
from dotenv import load_dotenv

#1 Security: Load the .env file
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ Error: API Key not found in .env file")
    exit()
    
#2 Setup: Configure the model
genai.configure(api_key = api_key)
model = genai.GenerativeModel('gemini-2.5-flash')

#3 User Input: The "Dynamic" part
print("\n ---🚀 YOUTUBE VIRALITY ENGINE---")
topic = input("Enter video topic (e.g. 'Python', 'Cooking'): ")
audience = input("Target Audience (e.g. 'Beginners', 'Experts'): ")

#4 The Prompt Template: This is where the engineering happens
# We give the AI a 'Persona' and 'Constraints'
prompt = f"""
Act as a viral marketing expert with 10 years of experience on YouTube.
I need 5 high-converting video titles for a video about: '{topic}'.
The target audience is: {audience}

Constraints:
1. Each title must have a 'Virality Score' from 1-100 based on psychological triggers.
2. Use strong hooks (e.g., 'Stop doing this', 'The Secret to').
3. Keep titles under 60 characters.
4. Output format: 
    1. [Title] (Score: XX/100)
    
Do not generate any intro text. Just the list.
"""

#5 Execute
print(f"\n... Analyzing trends for '{topic}'...\n")
try: 
    response = model.generate_content(prompt)
    print(response.text)
except Exception as e:
    print(f"❌ Error: {e}")
    
print("-"*40)