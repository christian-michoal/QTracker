import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
import time

# Hardcoded ticker
TICKER = "QTWO"

def get_stock_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period="1d", interval="1m")  # 1-minute interval for frequent updates
        return data
    except Exception as e:
        return None

# Streamlit App
st.set_page_config(page_title="Stock Price Tracker", layout="wide", initial_sidebar_state="collapsed")

# Custom CSS for responsive design and forcing light mode
st.markdown(
    """
    <style>
    .centered-title {
        text-align: center;
        font-size: 3rem;
        font-weight: bold;
        margin-top: 20px;
    }
    .centered-price {
        text-align: center;
        font-size: 4rem;
        font-weight: bold;
        margin-top: 10px;
    }
    .centered-change {
        text-align: center;
        font-size: 2.5rem;
        font-weight: bold;
        margin-top: 10px;
    }
    html, body, [class*="css"] {
        background-color: #ffffff !important;
        color: #000000 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Static Title
st.markdown(f"<div class='centered-title'>📈 Tracking: {TICKER}</div>", unsafe_allow_html=True)

# Separate placeholders for dynamic updates
price_placeholder = st.empty()
change_placeholder = st.empty()
chart_placeholder = st.empty()

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
            <div class="centered-price" style="color: {color};">
                ${latest_price:.2f}
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Update day's change
        change_placeholder.markdown(
            f"""
            <div class="centered-change" style="color: {color};">
                Day's Change: {change_percent:+.2f}%
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Create a static candlestick chart using Matplotlib
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(data.index, data['Close'], color='black', linewidth=1)

        # Add labels for the axes
        ax.set_title(f"{TICKER} Intraday Price", fontsize=14)
        ax.set_xlabel("Time", fontsize=12)
        ax.set_ylabel("Price ($)", fontsize=12)

        # Remove unnecessary decorations for a clean look
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        # Update chart dynamically
        chart_placeholder.pyplot(fig)

    time.sleep(10)  # Update every second
