import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

#1 Setup
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.5-flash')

#2 The Web Interface
st.title("🤖 Neha's AI Assistant")
st.subheader("Powered by Google Gemini 2.5")

#3 User Input (Text Box)
user_input = st.text_input("Ask me anything: ", placeholder = "Explain quantum physics...")

#4 The "Generate" Button:
if st.button("Generate Answer"):
    if user_input:
        with st.spinner("Thinking..."): # Shows a loading spinner
            response = model.generate_content(user_input)
            st.success("Here is your answer.")
            st.write(response.text) #Display the answer on the screen
    
    else:
        st.warning("Please enter a question first!")
        