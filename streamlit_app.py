import streamlit as st
import yfinance as yf
import time

# Set page configuration
st.set_page_config(page_title="QTracker", layout="wide", initial_sidebar_state="collapsed")

# Define a function to fetch stock data
def get_stock_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period="1d", interval="1m")  # 1-minute interval for frequent updates
        data.index = data.index.tz_localize(None)  # Remove timezone for cleaner data
        return data
    except Exception as e:
        return None

# Hardcoded ticker
TICKER = "QTWO"

# CSS for clean layout centering (horizontal only)
st.markdown(
    """
    <style>
    .centered-text {
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Display title
st.markdown(f"<h2 class='centered-text'>📈 Tracking: {TICKER}</h2>", unsafe_allow_html=True)

# Create placeholders for dynamic updates
price_placeholder = st.empty()
change_placeholder = st.empty()

while True:
    # Fetch stock data
    data = get_stock_data(TICKER)
    if data is not None:
        # Calculate price and change
        open_price = data['Open'].iloc[0]
        latest_price = data['Close'].iloc[-1]
        change_percent = ((latest_price - open_price) / open_price) * 100
        color = "green" if latest_price > open_price else "red"

        # Update price
        price_placeholder.markdown(
            f"""
            <div class="centered-text" style="font-size: 5rem; font-weight: bold; color: {color};">
                ${latest_price:.2f}
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Update day's change
        change_placeholder.markdown(
            f"""
            <div class="centered-text" style="font-size: 2.5rem; font-weight: bold; color: {color};">
                Day's Change: {change_percent:+.2f}%
            </div>
            """,
            unsafe_allow_html=True,
        )

    time.sleep(10)  # Update every 10 seconds
