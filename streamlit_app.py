import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
import time
from datetime import datetime

# Hardcoded ticker
TICKER = "QTWO"

def get_stock_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period="1d", interval="1m")  # Get intraday data
        return data
    except Exception as e:
        return None

# Streamlit App
st.set_page_config(page_title="Stock Price Tracker", layout="wide")

# Custom CSS for styling
st.markdown(
    """
    <style>
    .centered-title {
        text-align: center;
        font-size: 3.5rem;
        font-weight: bold;
        margin-top: 30px;
    }
    .centered-price {
        text-align: center;
        margin-top: 20px;
        font-size: 5rem;
        font-weight: bold;
    }
    .centered-change {
        text-align: center;
        margin-top: 10px;
        font-size: 3rem;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Centered Title
st.markdown(f"<div class='centered-title'>📈 Tracking: {TICKER}</div>", unsafe_allow_html=True)

# Placeholder for price, day's change, and chart
price_placeholder = st.empty()
change_placeholder = st.empty()
chart_placeholder = st.empty()

while True:
    # Get live price and data
    data = get_stock_data(TICKER)
    if data is not None:
        # Calculate the day's change
        open_price = data['Open'][0]
        latest_price = data['Close'].iloc[-1]
        change_percent = ((latest_price - open_price) / open_price) * 100

        # Determine color based on price movement
        color = "green" if latest_price > open_price else "red"

        # Plot minimal graph with dynamic resizing
        fig, ax = plt.subplots(figsize=(10, 2), dpi=100)  # Resize to flexibly fit
        ax.plot(data.index, data['Close'], color="black", linewidth=1)

        # Format x-axis for time (hours/minutes)
        ax.set_xticks(data.index[::60])  # Label every hour (approx.)
        ax.set_xticklabels([datetime.strftime(t, '%H:%M') for t in data.index[::60]], fontsize=8)

        # Format y-axis for stock prices
        ax.set_yticks([data['Close'].min(), (data['Close'].max() + data['Close'].min()) / 2, data['Close'].max()])
        ax.set_yticklabels([f"${price:.2f}" for price in ax.get_yticks()], fontsize=8)

        # Remove extra graph decorations
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        # Update placeholders
        with price_placeholder:
            st.markdown(
                f"""
                <div class="centered-price" style="color: {color};">
                    ${latest_price:.2f}
                </div>
                """,
                unsafe_allow_html=True,
            )
        with change_placeholder:
            st.markdown(
                f"""
                <div class="centered-change" style="color: {color};">
                    Day's Change: {change_percent:+.2f}%
                </div>
                """,
                unsafe_allow_html=True,
            )
        with chart_placeholder:
            st.pyplot(fig, clear_figure=True)

    time.sleep(10)  # Update every 10 seconds
