import streamlit as st
import os
import time
from dotenv import load_dotenv
from google import genai

# --- 1. SETUP & UI ---
st.set_page_config(page_title="Auto-Marketer", page_icon="🎌")
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

st.title("🎌 The Auto-Marketer Agent")
st.write("Upload a raw promotional video. The AI will autonomously generate your entire social media rollout.")

# --- 2. UPLOAD & INGESTION ---
uploaded_file = st.file_uploader("Upload Promo Video (MP4)", type=["mp4"])

if uploaded_file and st.button("Generate Campaign 🚀"):
    
    with st.spinner("1️⃣ Uploading video to AI Storage..."):
        temp_path = "temp_promo.mp4"
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.read())
            
        video_file = client.files.upload(file=temp_path)
        
        while video_file.state.name == "PROCESSING":
            time.sleep(3)
            video_file = client.files.get(name=video_file.name)
            
    st.success("✅ Video Processed! Generating social rollout...")
    st.write("---")
    
    # --- 3. MULTI-PROMPT GENERATION (Free Tier Friendly) ---
    model_id = 'gemini-2.5-flash'
    system_instruction = "You are an expert anime streetwear marketer. Your goal is to build hype, highlight the apparel, and drive community engagement."
    
    prompts = {
        "🎥 YouTube Description": "Write an engaging, SEO-optimized YouTube description for this streetwear drop. Include a hook.",
        "⏱️ Action Timestamps": "Extract 3 exact timestamps where graphics or key apparel are most visible so we can use them as YouTube Chapters.",
        "🐦 Viral Tweets": "Write 2 short, hype-building tweets for this video drop. Use relevant fashion/anime hashtags."
    }
    
    for title, prompt in prompts.items():
        st.subheader(title)
        with st.spinner(f"Drafting {title}..."):
            start_time = time.time()
            
            # THE FIX: Pass the video_file and system instruction directly into the contents array
            full_prompt = f"SYSTEM INSTRUCTION: {system_instruction}\n\nTASK: {prompt}"
            
            response = client.models.generate_content(
                model=model_id,
                contents=[video_file, full_prompt]
            )
            
            st.write(response.text)
            st.caption(f"⚡ Generated in {round(time.time() - start_time, 2)} seconds")
            
    # --- 4. CLEANUP ---
    client.files.delete(name=video_file.name)
    os.remove(temp_path)
    st.info("🧹 Cloud servers cleaned. Temporary files deleted.")