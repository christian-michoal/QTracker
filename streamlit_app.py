import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
import mplfinance as mpf
import time

# Set page configuration
st.set_page_config(page_title="Stock Tracker", layout="wide", initial_sidebar_state="collapsed")

# Define a function to fetch stock data
def get_stock_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period="1d", interval="1m")  # 1-minute interval for frequent updates
        data.index = data.index.tz_localize(None)  # Remove timezone for cleaner plotting
        return data
    except Exception as e:
        return None

# Initialize session state for the ticker
if "ticker" not in st.session_state:
    st.session_state["ticker"] = None

# If no ticker is set, show the landing page
if not st.session_state["ticker"]:
    st.title("📈 Welcome to QTracker!")
    st.write("Enter a ticker below to start tracking.")
    user_input = st.text_input("Enter Ticker", placeholder="e.g., QTWO, OZK")
    
    if st.button("Track Stock"):
        if user_input.strip():  # Ensure input is not empty
            st.session_state["ticker"] = user_input.strip().upper()  # Store the ticker in session state
            st.experimental_rerun()  # Refresh the page to go to the tracking view
else:
    # If a ticker is set, display the tracking page
    TICKER = st.session_state["ticker"]
    
    st.markdown(f"<div style='text-align: center; font-size: 3rem; font-weight: bold;'>📈 Tracking: {TICKER}</div>", unsafe_allow_html=True)

    # Create placeholders for dynamic updates
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
                <div style="text-align: center; font-size: 4rem; font-weight: bold; color: {color};">
                    ${latest_price:.2f}
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Update day's change
            change_placeholder.markdown(
                f"""
                <div style="text-align: center; font-size: 2.5rem; font-weight: bold; color: {color};">
                    Day's Change: {change_percent:+.2f}%
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Create a minimalist candlestick chart
            fig, ax = plt.subplots(figsize=(10, 4))

            # Prepare data for mplfinance
            data_for_plot = data[['Open', 'High', 'Low', 'Close']]

            # Create candlestick chart
            mpf.plot(
                data_for_plot,
                type='candle',
                ax=ax,
                style='charles',
                show_nontrading=False,
            )

            # Remove axis labels and unnecessary spines
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['bottom'].set_visible(False)
            ax.spines['left'].set_visible(False)
            ax.yaxis.set_visible(False)
            ax.xaxis.set_visible(False)

            # Update chart dynamically
            chart_placeholder.pyplot(fig)

        time.sleep(1)  # Update every second
