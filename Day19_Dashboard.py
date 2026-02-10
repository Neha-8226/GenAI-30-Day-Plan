import streamlit as st
import pandas as pd
import numpy as np
import time

# 1. Page Config
st.set_page_config(page_title="Agent Dashboard 📈", layout="wide")

# 2. Session State (The Fix: Use dictionary syntax)
if 'history' not in st.session_state:
    st.session_state['history'] = []  # <--- Dictionary syntax is safer

# 3. Sidebar
st.sidebar.title("🤖 Agent Controls")
ticker = st.sidebar.text_input("Enter Stock Ticker:", "AAPL").upper()
shares = st.sidebar.number_input("Shares Owned:", min_value=1, value=10)

# 4. The Logic
def get_stock_data(symbol):
    time.sleep(1) # Fake thinking
    base_price = np.random.uniform(100, 500)
    trend = np.linspace(0, 10, 20) + np.random.normal(0, 1, 20)
    prices = base_price + trend
    return round(prices[-1], 2), prices

# 5. The Main UI
st.title(f"📊 Live Analysis: {ticker}")

if st.sidebar.button("Analyze Stock 🚀"):
    with st.spinner(f"Agent is contacting the exchange for {ticker}..."):
        
        # Call Tool
        current_price, price_history = get_stock_data(ticker)
        total_value = current_price * shares
        
        # Save to History (Using dictionary syntax)
        new_entry = {
            "Ticker": ticker, 
            "Price": current_price, 
            "Value": total_value
        }
        st.session_state['history'].append(new_entry)

        # Metrics
        col1, col2, col3 = st.columns(3)
        col1.metric("Current Price", f"${current_price}")
        col2.metric("Your Holdings", f"${total_value:,.2f}")
        col3.metric("Day Change", f"{np.random.uniform(-5, 5):.2f}%")
        
        # Chart
        st.subheader("Price Trend (Last 30 Mins)")
        st.line_chart(pd.DataFrame(price_history, columns=["Price"]))

# 6. Display History
# Check if list is not empty
if len(st.session_state['history']) > 0:
    st.write("---")
    st.subheader("📜 Agent Activity Log")
    st.dataframe(pd.DataFrame(st.session_state['history']))