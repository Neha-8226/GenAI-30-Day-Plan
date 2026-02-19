import os
import time
from dotenv import load_dotenv
from google import genai

# 1. Setup
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

print("--- 🎙️ Initializing Voice AI (Native Audio Processing) ---")

# 2. Select your audio file
audio_path = "Audio.m4a" 

if not os.path.exists(audio_path):
    print(f"❌ Error: Could not find '{audio_path}'. Please place an MP3 or WAV in this folder.")
else:
    try:
        print(f"1️⃣ Uploading '{audio_path}' to Gemini Storage...")
        # The File API uploads the raw audio binary directly
        uploaded_audio = client.files.upload(file=audio_path)
        print(f"   ✅ Audio Uploaded! ID: {uploaded_audio.name}")
        
        # Poll for processing status (audio takes a moment to tokenize)
        while uploaded_audio.state.name == "PROCESSING":
            print("   ⏳ Processing audio waveform...")
            time.sleep(2)
            uploaded_audio = client.files.get(name=uploaded_audio.name)

        if uploaded_audio.state.name != "ACTIVE":
            raise Exception(f"File failed to process. State: {uploaded_audio.state.name}")

        print("2️⃣ Listening and analyzing tone, speech, and context...")
        
        # 3. The Multimodal Prompt
        # Notice how we ask for things a standard text transcript could never provide
        prompt = """
        You are an expert Audio Analyst. Listen to this recording carefully.
        1. TRANSCRIPT: Provide a clean transcript of what is being said.
        2. EMOTION & TONE: Describe the emotional tone of the speaker (e.g., excited, hesitant, frustrated).
        3. BACKGROUND: Describe any background noises, pauses, or sound effects you hear.
        """

        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[uploaded_audio, prompt]
        )

        print("\n🎧 [AI AUDIO ANALYSIS RESULT]:\n")
        print(response.text)

    except Exception as e:
        print(f"\n❌ Error: {e}")

    finally:
        # 4. Cleanup
        # Always delete media files from the cloud when done
        if 'uploaded_audio' in locals():
            client.files.delete(name=uploaded_audio.name)
            print("\n🧹 Cleanup: Audio file securely deleted from Google servers.")