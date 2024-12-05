import streamlit as st
import yfinance as yf
import time

def get_stock_price(ticker):
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period="1d")
        return data['Close'][-1]
    except Exception as e:
        return f"Error: {e}"

# Streamlit App UI
st.title("Real-Time Stock Ticker App")
st.subheader("Enter a stock ticker to view its price:")

ticker = st.text_input("Stock Ticker", value="AAPL", max_chars=10).upper()

if ticker:
    st.write(f"**Tracking stock price for:** {ticker}")
    placeholder = st.empty()
    while True:
        price = get_stock_price(ticker)
        placeholder.metric(label="Stock Price", value=f"${price:.2f}" if isinstance(price, (float, int)) else price)
        time.sleep(1)  # Update every 10 seconds
