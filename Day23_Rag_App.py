import streamlit as st
import numpy as np
import os
import time
from dotenv import load_dotenv
from google import genai

# 1. Setup API and Page
st.set_page_config(page_title="Data Chatbot", page_icon="📚")
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# 2. The Vector Database
if 'vector_db' not in st.session_state:
    st.session_state.vector_db = []

def get_embeddings_batch(text_list):
    """THE FIX: Sends all paragraphs to Google in ONE single API call!"""
    try:
        result = client.models.embed_content(
            model="gemini-embedding-001",
            contents=text_list # We pass the whole list at once!
        )
        # Returns a list of vectors
        return [emb.values for emb in result.embeddings]
    except Exception as e:
        st.error(f"Embedding Error: {e}")
        return []

def get_single_embedding(text):
    """Used just for the single question you type in."""
    try:
        result = client.models.embed_content(
            model="gemini-embedding-001",
            contents=text
        )
        return result.embeddings[0].values
    except Exception as e:
        return []

# --- 3. THE UI ---
st.title("📚 Chat with your Documents")
st.write("Upload a text file, and I will answer questions about it.")

# A. File Uploader
uploaded_file = st.file_uploader("Upload a .txt file", type=["txt"])

if uploaded_file and st.button("Process Document 🧠"):
    with st.spinner("Batch embedding document to save API quota..."):
        raw_text = uploaded_file.getvalue().decode("utf-8")
        chunks = [chunk.strip() for chunk in raw_text.split('\n\n') if len(chunk) > 10]
        
        st.session_state.vector_db = []
        
        # --- SEND THE BATCH ---
        vectors = get_embeddings_batch(chunks)
        
        if vectors and len(vectors) == len(chunks):
            # Save them to our database
            for i in range(len(chunks)):
                st.session_state.vector_db.append({"text": chunks[i], "vector": vectors[i]})
            st.success(f"Success! Embedded {len(chunks)} chunks using only ONE API call. 🤯")
        else:
            st.error("Failed to process document. Quota might be entirely exhausted.")

# B. Chat Interface
st.write("---")
user_question = st.text_input("Ask a question about the document:")

if user_question:
    if len(st.session_state.vector_db) == 0:
        st.warning("Please upload and process a document first!")
    else:
        with st.spinner("Searching database..."):
            
            # Adding a tiny pause so we don't trip the rate limit alarm
            time.sleep(2) 
            
            # 1. Embed the user's question
            query_vec = get_single_embedding(user_question)
            
            if query_vec:
                # 2. Find the best match
                scores = [np.dot(query_vec, entry['vector']) for entry in st.session_state.vector_db]
                best_idx = np.argmax(scores)
                best_context = st.session_state.vector_db[best_idx]['text']
                
                # 3. Augment and Generate
                prompt = f"""
                You are a helpful assistant. Answer the question based ONLY on this context.
                
                CONTEXT:
                {best_context}
                
                QUESTION:
                {user_question}
                """
                
                try:
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=prompt
                    )
                    
                    # 4. Show the result
                    st.info("💡 Found relevant info in your file!")
                    st.write(f"**Answer:** {response.text}")
                    
                    with st.expander("See the exact text retrieved from your file"):
                        st.write(best_context)
                        
                except Exception as e:
                    st.error(f"Generation Error: {e}")
            else:
                st.error("Could not embed the question. The API might need a 60-second break.")