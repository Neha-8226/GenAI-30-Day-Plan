import google.generativeai as genai
import os
from dotenv import load_dotenv

#1 Setup
load_dotenv() 
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key = api_key)
model = genai.GenerativeModel('gemini-2.5-flash')

# --- LINK 1: The Writer ---
def generate_story(topic):
    print(f"---✍️ Step 1: Generating story about '{topic}'---")
    prompt = f"Write a very short story, 2-sentence horror story about {topic}."
    response = model.generate_content(prompt)
    return response.text

# --- LINK 2: The Critic ---
def grade_story(story_text):
    print("\n 🧐 Step 2: Sending to Editor for Grading ---")
    prompt = f"""
    You are a strict Luterature Critic.
    Read the following story and rate it on a scale of 1-5 stars.
    
    STORY:
    {story_text}
    
    OUTPUT FORMAT:
    Stars: ⭐
    Feedback: (One short sentence)
    """
    
    response = model.generate_content(prompt)
    return response.text

# --- THE CHAIN (Main Execution) ---
user_topic = input("Enter a horror topic (e.g., 'A mirror'): ")

#1 Run Link 1
raw_story = generate_story(user_topic)
print(f"\n[DRAFT]: {raw_story}")

#2 Run Link 2 (Pass the output of Link 1 into Link 2)
final_grade = grade_story(raw_story)
print(f"\n[VERDICT]:\n{final_grade}")