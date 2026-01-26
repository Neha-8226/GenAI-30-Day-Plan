import google.generativeai as genai
import os
import time
from dotenv import load_dotenv

#1 Setup
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.5-flash')

#2 Upload the Audio File to Gemini's Server
# (This sends the file to Google so the AI can access it)
audio_path = "Audio.m4a" 
print(f"--- 🎤 Uploading {audio_path} ---")

audio_file = genai.upload_file(path = audio_path)

print(f"Upload Complete. File Name: {audio_file.name}")
print("Processing Audio... (This might take a few seconds)")

#3 The Prompt
prompt = "Listen to this audio clip. Transcribe what is said word-for-word, and then give a 1-sentence summary of the tone."

#4 Generate Content (Audio + Text)
response = model.generate_content([prompt, audio_file])

#5 Output
print("\n--- 📝 AI Transcription & Analysis ---")
print(response.text)