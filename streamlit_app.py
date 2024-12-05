import streamlit as st
import yfinance as yf
import time

# Hardcoded ticker
TICKER = "QTWO"  # Change this to your desired stock ticker

def get_stock_price(ticker):
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period="1d")
        return data['Close'][-1]
    except Exception as e:
        return f"Error: {e}"

# Streamlit App
st.set_page_config(page_title="Stock Price Tracker", layout="centered")
st.title(f"📈Tracking: {TICKER}")

placeholder = st.empty()

while True:
    price = get_stock_price(TICKER)
    with placeholder:
        st.markdown(
            f"""
            <div style="text-align: center; margin-top: 50px;">
                <h1 style="font-size: 4rem; font-weight: bold;">${price:.2f}</h1>
                <h2 style="font-size: 2rem; font-weight: bold;">{TICKER}</h2>
            </div>
            """,
            unsafe_allow_html=True,
        )
    time.sleep(10)  # Update every 10 seconds
