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
st.set_page_config(page_title="Stock Price Tracker", layout="wide")

# Custom CSS for alignment
st.markdown(
    """
    <style>
    .centered-title {
        text-align: center;
        font-size: 2.5rem;
        font-weight: bold;
        margin-top: 50px;
    }
    .centered-price {
        text-align: center;
        margin-top: 50px;
    }
    .price {
        font-size: 4rem;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Centered Title
st.markdown(f"<div class='centered-title'>📈 Tracking: {TICKER}</div>", unsafe_allow_html=True)

# Placeholder for price
placeholder = st.empty()

while True:
    price = get_stock_price(TICKER)
    with placeholder:
        st.markdown(
            f"""
            <div class="centered-price">
                <span class="price">${price:.2f}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
    time.sleep(10)  # Update every 10 seconds
