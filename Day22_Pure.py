import os
import json
import numpy as np
from dotenv import load_dotenv
from google import genai

# 1. Setup Gemini
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

print("--- 🚀 System Starting: Pure Python Vector DB ---")

def get_embedding(text):
    """Turns text into a list of numbers (vector) using the latest model."""
    try:
        # Using the new, currently active Gemini Embedding model
        result = client.models.embed_content(
            model="gemini-embedding-001", # <--- THE MAGIC FIX
            contents=text
        )
        return result.embeddings[0].values
    except Exception as e:
        print(f"   ❌ Error getting embedding: {e}")
        return []

# 2. Build the Database Class (Using JSON, not Chroma)
class PureVectorDB:
    def __init__(self, filename="my_pure_db.json"):
        self.filename = filename
        self.data = []
        self.load_db()

    def load_db(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                self.data = json.load(f)
            print(f"📂 Database Loaded: {len(self.data)} records.")
        else:
            print("🆕 Created new empty database.")

    def save_db(self):
        with open(self.filename, 'w') as f:
            json.dump(self.data, f)
        print("💾 Database Saved.")

    def add(self, text):
        print(f"   Embedding: '{text}'...")
        vector = get_embedding(text)
        if vector:
            self.data.append({"text": text, "vector": vector})
            self.save_db()

    def search(self, query):
        print(f"\n🔎 Searching for: '{query}'...")
        query_vec = get_embedding(query)
        
        if not query_vec: 
            return "Error: Could not embed the search query."

        scores = []
        for entry in self.data:
            # DOT PRODUCT (The Math of Similarity)
            score = np.dot(query_vec, entry['vector'])
            scores.append(score)
        
        # Find the index of the highest score
        best_idx = np.argmax(scores)
        return self.data[best_idx]['text']

# --- 3. RUN IT ---
db = PureVectorDB()

# Only add data if the DB is empty
if len(db.data) == 0:
    print("\n--- 📥 Adding Knowledge ---")
    docs = [
        "The heavy rain is causing flooding in the streets.",
        "The stock market crashed due to inflation fears.",
        "My iPhone battery drains too fast after the update.",
        "The chef prepared a spicy curry with fresh herbs."
    ]
    for d in docs:
        db.add(d)

# Test the Search
if len(db.data) > 0:
    result = db.search("My device is not working well")
    print(f"\n✅ BEST MATCH: \"{result}\"")
else:
    print("\n❌ No data in database to search.")