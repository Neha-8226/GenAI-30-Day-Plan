import google.generativeai as genai
import os
from dotenv import load_dotenv
from PIL import Image # This helps Python "see" the image file

#1 Setup
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

#2 Use the Flash model (it is very fast at vision tasks)
model = genai.GenerativeModel('gemini-2.5-flash')

#3 Load the image
# Make sure the name matches YOUR file exactly
image_path = "test_image.jpg" 
img = Image.open(image_path)

print("--- 👁️ AI Vision Analyst ---")
print(f"Analyzing {image_path}...")

#4 The Magic: Send text AND image together 
prompt = "Analyze this image. Describe what you see in detail and list 3 interesting facts about it."

response = model.generate_content([prompt, img])

#5 Print the Results
print("\nAI Analysis: ")
print(response.text)