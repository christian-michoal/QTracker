import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
import time

# Hardcoded ticker
TICKER = "AAPL"  # Change this to your desired stock ticker

def get_stock_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period="1d", interval="1m")  # Get intraday data
        return data
    except Exception as e:
        return None, f"Error: {e}"

# Streamlit App
st.set_page_config(page_title="Stock Price Tracker", layout="wide")

# Custom CSS for styling
st.markdown(
    """
    <style>
    .centered-title {
        text-align: center;
        font-size: 2.5rem;
        font-weight: bold;
        margin-top: 30px;
    }
    .centered-price {
        text-align: center;
        margin-top: 20px;
    }
    .price {
        font-size: 4rem;
        font-weight: bold;
    }
    .minimal-graph {
        margin-top: 30px;
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Centered Title
st.markdown(f"<div class='centered-title'>📈 Tracking: {TICKER}</div>", unsafe_allow_html=True)

# Placeholder for price and chart
price_placeholder = st.empty()
chart_placeholder = st.empty()

while True:
    # Get live price and data
    data = get_stock_data(TICKER)
    if data is not None:
        # Latest price
        price = data['Close'].iloc[-1]

        # Plot minimal graph
        fig, ax = plt.subplots(figsize=(6, 2))  # Small graph
        ax.plot(data['Close'], color="black", linewidth=1)
        ax.set_xticks([])  # Remove x-axis ticks
        ax.set_yticks([])  # Remove y-axis ticks
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)

        # Update placeholders
        with price_placeholder:
            st.markdown(
                f"""
                <div class="centered-price">
                    <span class="price">${price:.2f}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with chart_placeholder:
            st.pyplot(fig)

    time.sleep(10)  # Update every 10 seconds
