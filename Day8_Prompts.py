import google.generativeai as genai
import os
from dotenv import load_dotenv

#1 Setup
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key = api_key)
model = genai.GenerativeModel('gemini-2.5-flash')

#2 The Prompt Engine Function
def generate_video_script(topic, audience, tone):
    print(f"---🎥 Generating Script for: {topic}---")
    
    # The MASTER TEMPLATE
    # We use f""" to insert our variables dynamically
    prompt = f"""
    ROLE: You are a professional Youtuber with 1M+ subscribers.add()
    
    CONTEXT: I need a script for a video about "{topic}".
    TARGET AUDIENCE: {audience}
    TONE: {tone}
    
    TASK: Write a structured video script.
    
    FORMAT:
    1. Hook (0-10s): Grab attention immediately.
    2. Intro (10-30s): State the problem.
    3. Body (3 Main Points): Explain clearly with examples.
    4. Call to Action: Ask for likes/subscribes.
    
    OUTPUT CONSTRAINT: Return ONLY the script. Do not say "Here is your script."
    """
    
    response = model.generate_content(prompt)
    return response.text

#3 User Input (The "Variables")
my_topic = input("Enter Video Topic: ")
my_audience = input("Enter Target Audience: ")
my_tone = input("Enter Tone (e.g., Funny, Serious): ")

#4 Run the machine
script = generate_video_script(my_topic, my_audience, my_tone)

print("\n---✨ YOUR GENERATED SCRIPT ✨---")
print(script)