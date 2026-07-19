import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from src.data import extract_stock_symbol, fetch_history, normalize_symbol
from src.indicators import add_indicators
from src.metrics import performance_summary, rsi_signal, trend_signal
from src.reporting import build_text_report


st.set_page_config(page_title="Financial Research AI Agent", layout="wide")


@st.cache_data(ttl=900, show_spinner=False)
def cached_history(symbol, period):
    return fetch_history(symbol, period)


def price_chart(data, symbol):
    fig = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        row_heights=[0.72, 0.28],
        vertical_spacing=0.05,
        subplot_titles=(f"{symbol} price action", "Volume"),
    )
    fig.add_trace(
        go.Candlestick(
            x=data.index,
            open=data["Open"],
            high=data["High"],
            low=data["Low"],
            close=data["Close"],
            name="Price",
        ),
        row=1,
        col=1,
    )
    fig.add_trace(
        go.Scatter(x=data.index, y=data["SMA20"], name="SMA 20", line={"width": 1.5}),
        row=1,
        col=1,
    )
    fig.add_trace(
        go.Scatter(x=data.index, y=data["SMA50"], name="SMA 50", line={"width": 1.5}),
        row=1,
        col=1,
    )
    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data["BB_UPPER"],
            name="Bollinger upper",
            line={"width": 1, "dash": "dot"},
        ),
        row=1,
        col=1,
    )
    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data["BB_LOWER"],
            name="Bollinger lower",
            line={"width": 1, "dash": "dot"},
        ),
        row=1,
        col=1,
    )
    fig.add_trace(
        go.Bar(x=data.index, y=data["Volume"], name="Volume", marker_color="#6b7280"),
        row=2,
        col=1,
    )
    fig.update_layout(height=680, xaxis_rangeslider_visible=False, margin={"t": 60})
    fig.update_yaxes(title_text="Price", row=1, col=1)
    fig.update_yaxes(title_text="Volume", row=2, col=1)
    return fig


def rsi_chart(data):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.index, y=data["RSI"], name="RSI", line={"width": 2}))
    fig.add_hline(y=70, line_dash="dash", line_color="#ef4444")
    fig.add_hline(y=30, line_dash="dash", line_color="#22c55e")
    fig.update_layout(height=320, yaxis_range=[0, 100], margin={"t": 20})
    return fig


def macd_chart(data):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.index, y=data["MACD"], name="MACD"))
    fig.add_trace(go.Scatter(x=data.index, y=data["MACD_SIGNAL"], name="Signal"))
    fig.add_trace(go.Bar(x=data.index, y=data["MACD_HIST"], name="Histogram"))
    fig.update_layout(height=320, margin={"t": 20})
    return fig


def comparison_chart(series_map):
    fig = go.Figure()

    for symbol, data in series_map.items():
        if data is None or data.empty:
            continue

        normalized = data["Close"] / data["Close"].iloc[0] * 100
        fig.add_trace(go.Scatter(x=data.index, y=normalized, name=symbol))

    fig.update_layout(
        title="Normalized performance comparison",
        yaxis_title="Indexed value, first day = 100",
        height=480,
    )
    return fig


st.title("Financial Research AI Agent")
st.caption("Advanced Streamlit research dashboard for Indian equity analysis.")
st.warning("Educational analysis only. This app does not provide investment advice.")

with st.container():
    col_a, col_b, col_c, col_d = st.columns([1.2, 1.2, 1.2, 0.8])

    with col_a:
        symbol_input = st.text_input("Primary stock", "RELIANCE.NS")

    with col_b:
        compare_input = st.text_input("Compare stock", "TCS.NS")

    with col_c:
        benchmark_input = st.text_input("Benchmark", "^NSEI")

    with col_d:
        period = st.selectbox("Period", ["1mo", "3mo", "6mo", "1y", "2y", "5y"], index=3)

    analyze = st.button("Run research", type="primary", use_container_width=True)


chat_question = st.text_input(
    "Stock price chatbot",
    "What is the latest price of RELIANCE.NS?",
)

if st.button("Ask chatbot"):
    chatbot_symbol = extract_stock_symbol(chat_question)

    if chatbot_symbol is None:
        st.error("Include a symbol like RELIANCE.NS, TCS.NS, INFY.NS, or HDFCBANK.NS.")
    else:
        chatbot_data = cached_history(chatbot_symbol, "5d")

        if chatbot_data.empty:
            st.error(f"No recent data found for {chatbot_symbol}.")
        else:
            price = chatbot_data["Close"].iloc[-1]
            date = chatbot_data.index[-1].date()
            st.success(f"{chatbot_symbol} latest close was INR {price:.2f} on {date}.")


if not analyze:
    st.info("Run research to load market data, indicators, comparison, risk metrics, and report export.")
    st.stop()


symbol = normalize_symbol(symbol_input)
compare_symbol = normalize_symbol(compare_input) if compare_input else ""
benchmark_symbol = benchmark_input.strip().upper()

data = cached_history(symbol, period)
compare_data = cached_history(compare_symbol, period) if compare_symbol else None
benchmark_data = cached_history(benchmark_symbol, period) if benchmark_symbol else None

if data.empty:
    st.error("No data found. Try RELIANCE.NS, TCS.NS, INFY.NS, HDFCBANK.NS, or SBIN.NS.")
    st.stop()

data = add_indicators(data)
summary = performance_summary(data)
latest_price = data["Close"].iloc[-1]
latest_rsi = data["RSI"].dropna().iloc[-1] if not data["RSI"].dropna().empty else None

overview, charts, risk, compare, export = st.tabs(
    ["Overview", "Charts", "Risk", "Comparison", "Export"]
)

with overview:
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Latest close", f"INR {latest_price:.2f}")
    col2.metric("Total return", f"{summary['total_return']:.2%}")
    col3.metric("Annual volatility", f"{summary['annual_volatility']:.2%}")
    col4.metric("Max drawdown", f"{summary['max_drawdown']:.2%}")

    col5, col6, col7 = st.columns(3)
    col5.metric("Sharpe ratio", f"{summary['sharpe_ratio']:.2f}")
    col6.metric("Trend", trend_signal(data))
    col7.metric("RSI signal", rsi_signal(latest_rsi))

    st.dataframe(
        data[["Open", "High", "Low", "Close", "Volume", "SMA20", "SMA50", "RSI", "MACD"]]
        .tail(15)
        .round(2),
        use_container_width=True,
    )

with charts:
    st.plotly_chart(price_chart(data, symbol), use_container_width=True)
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("RSI")
        st.plotly_chart(rsi_chart(data), use_container_width=True)

    with col_right:
        st.subheader("MACD")
        st.plotly_chart(macd_chart(data), use_container_width=True)

with risk:
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Best day", f"{summary['best_day']:.2%}")
    col2.metric("Worst day", f"{summary['worst_day']:.2%}")
    col3.metric("Average daily return", f"{summary['average_daily_return']:.2%}")
    col4.metric("Positive days", f"{summary['positive_day_ratio']:.2%}")

    drawdown = data["Close"] / data["Close"].cummax() - 1
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.index, y=drawdown, fill="tozeroy", name="Drawdown"))
    fig.update_layout(height=420, yaxis_tickformat=".0%", yaxis_title="Drawdown")
    st.plotly_chart(fig, use_container_width=True)

with compare:
    series_map = {symbol: data}

    if compare_data is not None and not compare_data.empty:
        series_map[compare_symbol] = add_indicators(compare_data)

    if benchmark_data is not None and not benchmark_data.empty:
        series_map[benchmark_symbol] = add_indicators(benchmark_data)

    st.plotly_chart(comparison_chart(series_map), use_container_width=True)

    metric_rows = []
    for item_symbol, item_data in series_map.items():
        item_summary = performance_summary(item_data)
        metric_rows.append(
            {
                "Symbol": item_symbol,
                "Total Return": f"{item_summary['total_return']:.2%}",
                "Annual Volatility": f"{item_summary['annual_volatility']:.2%}",
                "Max Drawdown": f"{item_summary['max_drawdown']:.2%}",
                "Sharpe": f"{item_summary['sharpe_ratio']:.2f}",
            }
        )

    st.dataframe(metric_rows, use_container_width=True)

with export:
    report = build_text_report(symbol, data, summary, latest_rsi)
    st.text_area("Research summary", report, height=260)
    st.download_button(
        "Download indicator CSV",
        data.to_csv().encode("utf-8"),
        file_name=f"{symbol.replace('.', '_')}_research.csv",
        mime="text/csv",
    )
    st.download_button(
        "Download text report",
        report.encode("utf-8"),
        file_name=f"{symbol.replace('.', '_')}_report.txt",
        mime="text/plain",
    )
