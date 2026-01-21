import google.generativeai as genai
import os

# 1. SETUP: Paste your key here
api_key = "AIzaSyC_6ugHGb_eOMw9-LCpw1uc0V7SCbsclOw"
genai.configure(api_key=api_key)

print("--- CONTACTING GOOGLE SERVERS ---")
print("Asking for available models...")

try:
    # 2. ASK: List everything available to this API key
    for m in genai.list_models():
        # Only show models that can generate text (Chat models)
        if 'generateContent' in m.supported_generation_methods:
            print(f"FOUND: {m.name}")

except Exception as e:
    print(f"CRITICAL ERROR: {e}")

print("---------------------------------")