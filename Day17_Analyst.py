from google import genai
from google.genai import types
import os
import base64
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
def analyze_data(data_string, prompt):
    print(f"--- 📊 Analyst Working on: {prompt} ---")
    
    full_prompt = f"""
    Here is a CSV dataset:
    {data_string}
    
    Task: {prompt}
    
    IMPORTANT: 
    1. Use 'matplotlib' to generate the graph.
    2. YOU MUST USE 'plt.show()' at the end. 
    3. Do NOT just save it. Display it so I can download it.
    """

    try:
        # Use the reliable model
        response = client.models.generate_content(
            model='gemini-flash-latest',
            contents=full_prompt,
            config=types.GenerateContentConfig(
                tools=[{'code_execution': {}}] 
            )
        )
        
        # 4. FIND AND SAVE THE IMAGE
        image_found = False
        if response.candidates and response.candidates[0].content.parts:
            for part in response.candidates[0].content.parts:
                
                # Print code logic
                if part.executable_code:
                    print(f"\n[🤖 CODE]:\n{part.executable_code.code}")
                
                # CAPTURE THE IMAGE
                if part.inline_data and 'image' in part.inline_data.mime_type:
                    print("\n[📉 GRAPH RECEIVED] Downloading...")
                    
                    # Convert raw data to file
                    img_data = base64.b64decode(part.inline_data.data)
                    with open("sales_graph_final.png", "wb") as f:
                        f.write(img_data)
                    print("✅ SUCCESS: Saved 'sales_graph_final.png'!")
                    image_found = True

        if not image_found:
            print("⚠️ No graph returned. The AI might have skipped plt.show().")

    except Exception as e:
        print(f"Error: {e}")

# --- TEST IT ---
user_request = "Create a Bar Chart showing Total Sales by Product."
analyze_data(csv_content, user_request)