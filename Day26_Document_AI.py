import os
import time
from dotenv import load_dotenv
from google import genai

#1 Setup
load_dotenv()
client = genai.Client(api_key = os.getenv("GEMINI_API_KEY"))

print("---📝 Native Document AI (Multimodal)---")

#2 Select your file (Make sure this file exists!)
# Try a Resume, an Invoice, or a Financial Report with tables
file_path = "sample.pdf"

if not os.path.exists(file_path):
    print(f"❌ Error: Could not find '{file_path}'. Please place a PDF in this folder.")
else:
    try:
        print(f"1️⃣ Uploading '{file_path}' to Gemini Storage...")
        # Upload the file securely
        uploaded_file = client.files.upload(file = file_path)
        print(f" ✅ File Uploaded! ID: {uploaded_file.name}")
        
        # Poll for processing status (Big files take a second to 'tokenize')
        while uploaded_file.state.name == "PROCESSING":
            print("  ⏳ Processing file pixels...")
            time.sleep(2)
            uploaded_file=client.files.get(name=uploaded_file.name)
            
        if uploaded_file.state.name != "ACTIVE":
            raise Exception(f"File failed to process. State: {uploaded_file.state.name}")
        
        print("2️⃣ Analyzing document visual structure... ")
        
        #3 The Multimodal Prompt
        # We can ask about charts, tables, and layout because the AI 'sees' the page.
        prompt = """
        You are a Senior Data Analyst. Analyze this document.
        
        1. SUMMARY: Give a 2-sentence executive summary of what this file is.
        2. DATA EXTRACTION: If there are tables or financial numbers, extract them into a clean Markdown table.
        3. VISUALS: If there are any charts/graphs, describe exactly what trends they show.
        """
        
        response = client.models.generate_content(
            model = "gemini-2.5-flash",
            contents = [uploaded_file, prompt]
        )
        
        print("\n📊 [AI ANALYSIS RESULT]:\n")
        print(response.text)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        
    finally: 
        #4 Cleanup (Best Practice)
        # Always delete the file from the cloud when done to protect privacy
        if 'uploaded_file' in locals():
            client.files.delete(name=uploaded_file.name)
            print("\n🧹 Cleanup: File securely deleted from Google servers.")