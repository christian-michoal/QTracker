import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
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

# Custom CSS for responsive design
st.markdown(
    """
    <style>
    .centered-title {
        text-align: center;
        font-size: 3rem; /* Default for web */
        font-weight: bold;
        margin-top: 20px;
    }
    .centered-price {
        text-align: center;
        font-size: 4rem; /* Default for web */
        font-weight: bold;
        margin-top: 10px;
    }
    .centered-change {
        text-align: center;
        font-size: 2.5rem; /* Default for web */
        font-weight: bold;
        margin-top: 10px;
    }
    @media (max-width: 768px) {
        .centered-title { font-size: 2rem; } /* Adjust for smaller screens */
        .centered-price { font-size: 3rem; }
        .centered-change { font-size: 2rem; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Centered Title
st.markdown(f"<div class='centered-title'>📈 Tracking: {TICKER}</div>", unsafe_allow_html=True)

# Placeholders for live data
price_placeholder = st.empty()
change_placeholder = st.empty()
chart_placeholder = st.empty()

while True:
    # Fetch latest data
    data = get_stock_data(TICKER)
    if data is not None:
        # Calculate the day's change
        open_price = data['Open'][0]
        latest_price = data['Close'].iloc[-1]
        change_percent = ((latest_price - open_price) / open_price) * 100

        # Determine color based on price movement
        color = "green" if latest_price > open_price else "red"

        # Create candlestick chart
        fig = go.Figure(
            data=[
                go.Candlestick(
                    x=data.index,
                    open=data['Open'],
                    high=data['High'],
                    low=data['Low'],
                    close=data['Close'],
                    increasing_line_color='green',
                    decreasing_line_color='red',
                )
            ]
        )
        fig.update_layout(
            xaxis_rangeslider_visible=False,
            template="plotly_white",
            height=450 if st.config.get_option("theme.display_mode") == "dark" else 400,
            margin=dict(l=10, r=10, t=10, b=10),
        )

        # Update price and change
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

        # Update chart
        with chart_placeholder:
            st.plotly_chart(fig, use_container_width=True)

    time.sleep(1)  # Update as frequently as possible (every second)
