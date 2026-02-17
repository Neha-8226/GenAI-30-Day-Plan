import streamlit as st
import os
import time
from dotenv import load_dotenv
from google import genai

# 1. Setup
st.set_page_config(page_title="Streaming AI", page_icon="🌊")
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

st.title("🌊 Real-Time AI Streaming")
st.write("Notice how the text appears instantly, rather than waiting for the whole response!")

# 2. Chat History State
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 3. The Chat Input
if prompt := st.chat_input("Ask me to write a long essay or a Python script..."):
    
    # Add user message to UI and history
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Add AI response to UI
    with st.chat_message("assistant"):
        # We use st.empty() to create a placeholder box on the screen
        message_placeholder = st.empty()
        full_response = ""
        
        with st.spinner("Thinking..."):
            # THE MAGIC: We use _stream instead of normal generation!
            response_stream = client.models.generate_content_stream(
                model='gemini-2.5-flash',
                contents=prompt
            )
            
            # Loop through the stream as the chunks arrive over the internet
            for chunk in response_stream:
                if chunk.text:
                    full_response += chunk.text
                    # Update the placeholder instantly with the new text chunk
                    message_placeholder.markdown(full_response + "▌")
                    time.sleep(0.02) # Tiny artificial delay to make the typewriter effect smooth
            
            # Remove the cursor block when finished
            message_placeholder.markdown(full_response)
            
    # Save the final AI response to history
    st.session_state.messages.append({"role": "assistant", "content": full_response})