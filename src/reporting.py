from src.metrics import rsi_signal, trend_signal


def build_text_report(symbol, data, summary, latest_rsi):
    latest_close = data["Close"].iloc[-1]
    latest_date = data.index[-1].date()

    return "\n".join(
        [
            f"Financial Research Report: {symbol}",
            f"Latest close: INR {latest_close:,.2f} on {latest_date}",
            f"Total return: {summary['total_return']:.2%}",
            f"Annual volatility: {summary['annual_volatility']:.2%}",
            f"Maximum drawdown: {summary['max_drawdown']:.2%}",
            f"Sharpe ratio: {summary['sharpe_ratio']:.2f}",
            f"Trend signal: {trend_signal(data)}",
            f"RSI signal: {rsi_signal(latest_rsi)}",
            "",
            "Disclaimer: This report is educational analysis only and is not investment advice.",
        ]
    )
