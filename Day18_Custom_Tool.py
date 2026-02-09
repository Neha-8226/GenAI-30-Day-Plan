from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

# 1. Setup
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# 2. Define YOUR Custom Tools (The "Mock" APIs)

def get_stock_price(ticker: str):
    """
    Returns the current price of a stock.
    Args:
        ticker: The stock symbol (e.g., 'AAPL', 'GOOGL').
    """
    print(f"\n[🔌 API TRIGGERED] Fetching price for: {ticker}")
    prices = {"AAPL": 150, "GOOGL": 2800, "TSLA": 700}
    return prices.get(ticker.upper(), 100)

def get_user_balance(user_id: str):
    """
    Returns the bank balance for a specific user.
    Args:
        user_id: The ID of the user (e.g., 'U123').
    """
    print(f"\n[🔌 API TRIGGERED] Checking balance for: {user_id}")
    if user_id == "U123":
        return 2000
    return 0

# 3. Create the Agent with Tools
my_tools = [get_stock_price, get_user_balance]

def ask_broker(user_query):
    print(f"--- 💼 Broker Agent: '{user_query}' ---")

    # FIXED CONFIG: We removed 'automatic_function_calling'
    # The model defaults to "Auto" mode anyway!
    config = types.GenerateContentConfig(
        tools=my_tools 
    )

    try:
        response = client.models.generate_content(
            model='gemini-flash-latest',
            contents=user_query,
            config=config
        )
        return response.text

    except Exception as e:
        return f"Error: {e}"

# --- TEST IT ---
query = "I am user U123. Can I afford to buy 10 shares of AAPL?"
final_answer = ask_broker(query)

print("\n--- 📝 Final Answer ---")
print(final_answer)