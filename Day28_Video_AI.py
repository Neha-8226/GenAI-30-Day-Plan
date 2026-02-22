import os
import time
from dotenv import load_dotenv
from google import genai

# 1. Setup
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

print("--- 🎬 Initializing Native Video AI ---")

# 2. Select your video file
video_path = "sample.mp4" 

if not os.path.exists(video_path):
    print(f"❌ Error: Could not find '{video_path}'. Please place an MP4 in this folder.")
else:
    try:
        print(f"1️⃣ Uploading '{video_path}' to Gemini Storage...")
        uploaded_video = client.files.upload(file=video_path)
        print(f"   ✅ Video Uploaded! ID: {uploaded_video.name}")
        
        # Poll for processing status (Video tokenization takes time!)
        while uploaded_video.state.name == "PROCESSING":
            print("   ⏳ Watching video frames and syncing audio... (This may take a minute)")
            time.sleep(5)
            uploaded_video = client.files.get(name=uploaded_video.name)

        if uploaded_video.state.name != "ACTIVE":
            raise Exception(f"Video failed to process. State: {uploaded_video.state.name}")

        print("2️⃣ Video successfully processed! Analyzing timeline and visuals...")
        
        # 3. The Multimodal Prompt
        prompt = """
        You are an expert Video Director and Analyst. Watch this video carefully.
        1. SUMMARY: Provide a 2-sentence summary of the video's core message.
        2. TIMESTAMPS: Map out 3 to 4 key visual moments in the video with their exact timestamps (e.g., 0:15 - The camera pans to a close-up).
        3. CINEMATOGRAPHY: Describe the lighting and camera movement style.
        """

        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[uploaded_video, prompt]
        )

        print("\n🎞️ [AI VIDEO ANALYSIS RESULT]:\n")
        print(response.text)

    except Exception as e:
        print(f"\n❌ Error: {e}")

    finally:
        # 4. Cleanup
        if 'uploaded_video' in locals():
            client.files.delete(name=uploaded_video.name)
            print("\n🧹 Cleanup: Video file securely deleted from Google servers.")