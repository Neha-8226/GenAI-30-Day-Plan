import google.generativeai as genai
import os
from dotenv import load_dotenv

#1 Setup
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key = api_key)
model = genai.GenerativeModel('gemini-2.5-flash')

#2 Define the Few-Shot Prompt
# NOTICE: We use {{}} for JSON so Python doesn't confuse it with variables!
few_shot_prompt = """
SYSTEM: You are an AI that extracts specific data from customer reviews.
Return the output in this format: {{"Sentiment": "Pos/Neg", "Product": "Name", "Key_Issue": "Short Summary"}}

EXAMPLE 1:
Input: "I loved the iPhone 15, the camera is amazing but it gets hot."
Output: {{"Sentiment": "Mixed", "Product": "iPhone 15", "Key_Issue": "Overheating"}}

EXAMPLE 2:
Input: "The pizza arrived cold and the delivery guy was rude."
Output: {{"Sentiment": "Negative", "Product": "Pizza", "Key_Issue": "Delivery Service"}}

EXAMPLE 3:
Input: "My Nike Shoes are super comfortable for running."
Output: {{"Sentiment": "Positive", "Product": "Nike Shoes", "Key_Issue": "None"}}

USER INPUT (Your Turn):
Input: "{user_review}"
Output: 
"""

def classify_review(review_text):
    # Inject the user's input into the pattern
    final_prompt = few_shot_prompt.format(user_review = review_text)
    
    response = model.generate_content(final_prompt)
    return response.text

#3 Test it
print("---🧠 Few-Shot Logic Tester ---")
print("Enter a product review (e.g., 'The laptop is fast but the screen is dim')")
user_input = input("Review: ")

result = classify_review(user_input)

print("\n---AI Extracted Data ---")
print(result)