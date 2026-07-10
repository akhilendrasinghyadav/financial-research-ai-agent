import streamlit as st
import yfinance as yf
import plotly.graph_objects as go


st.set_page_config(page_title="Financial Research AI Agent", layout="wide")

st.title("Financial Research AI Agent")
st.caption("Week 1-2 demo: Indian stock price analysis, RSI, moving average, and comparison.")
st.warning("This is educational financial analysis, not investment advice.")

with st.sidebar:
    st.header("Inputs")
    symbol = st.text_input("Enter stock symbol", "RELIANCE.NS").strip().upper()
    compare_symbol = st.text_input("Compare with another stock", "TCS.NS").strip().upper()
    period = st.selectbox("Select period", ["1mo", "3mo", "6mo", "1y", "5y"], index=3)
    analyze = st.button("Analyze", type="primary")


def calculate_rsi(close_prices, window=14):
    delta = close_prices.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window).mean()
    avg_loss = loss.rolling(window).mean()
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))


def fetch_stock_history(stock_symbol, selected_period):
    try:
        return yf.Ticker(stock_symbol).history(period=selected_period)
    except Exception as error:
        st.error(f"Could not fetch data for {stock_symbol}: {error}")
        return None


if analyze:
    if not symbol:
        st.error("Please enter a stock symbol, for example RELIANCE.NS.")
        st.stop()

    data = fetch_stock_history(symbol, period)
    compare_data = fetch_stock_history(compare_symbol, period) if compare_symbol else None

    if data is None or data.empty:
        st.error("No data found. Try RELIANCE.NS, TCS.NS, INFY.NS, or HDFCBANK.NS.")
    else:
        latest_price = data["Close"].iloc[-1]
        data["SMA20"] = data["Close"].rolling(20).mean()
        data["RSI"] = calculate_rsi(data["Close"])

        col1, col2, col3 = st.columns(3)
        col1.metric("Stock", symbol)
        col2.metric("Latest Close Price", f"INR {latest_price:.2f}")
        col3.metric("Selected Period", period)

        st.subheader(f"{symbol} Price Chart")

        fig = go.Figure()
        fig.add_trace(go.Candlestick(
            x=data.index,
            open=data["Open"],
            high=data["High"],
            low=data["Low"],
            close=data["Close"],
            name="Price"
        ))
        fig.add_trace(go.Scatter(
            x=data.index,
            y=data["SMA20"],
            name="20 Day Moving Average"
        ))
        fig.update_layout(
            title=f"{symbol} Stock Price",
            xaxis_title="Date",
            yaxis_title="Price",
            height=600
        )
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("RSI Indicator")
        rsi_values = data["RSI"].dropna()

        if rsi_values.empty:
            st.info("RSI needs more price history. Select 3mo, 6mo, or 1y.")
        else:
            st.line_chart(data["RSI"])
            latest_rsi = rsi_values.iloc[-1]

            if latest_rsi > 70:
                st.warning("RSI is above 70. The stock may be in an overbought zone.")
            elif latest_rsi < 30:
                st.warning("RSI is below 30. The stock may be in an oversold zone.")
            else:
                st.success("RSI is in the normal range.")

        st.subheader("Basic Analysis")
        st.write(f"{symbol} latest closing price is INR {latest_price:.2f}.")
        st.write("Indian NSE symbols usually end with .NS, for example RELIANCE.NS or TCS.NS.")

        if compare_data is not None and not compare_data.empty:
            st.subheader("Stock Comparison")

            comparison_fig = go.Figure()
            comparison_fig.add_trace(go.Scatter(
                x=data.index,
                y=data["Close"],
                name=symbol
            ))
            comparison_fig.add_trace(go.Scatter(
                x=compare_data.index,
                y=compare_data["Close"],
                name=compare_symbol
            ))
            comparison_fig.update_layout(
                title=f"{symbol} vs {compare_symbol}",
                xaxis_title="Date",
                yaxis_title="Closing Price",
                height=500
            )
            st.plotly_chart(comparison_fig, use_container_width=True)

            first_price = latest_price
            second_price = compare_data["Close"].iloc[-1]

            col1, col2 = st.columns(2)
            col1.metric(symbol, f"INR {first_price:.2f}")
            col2.metric(compare_symbol, f"INR {second_price:.2f}")
else:
    st.info("Enter stock symbols in the sidebar and click Analyze.")
