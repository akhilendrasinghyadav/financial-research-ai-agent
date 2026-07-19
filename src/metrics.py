import math


def performance_summary(data):
    close = data["Close"].dropna()
    returns = close.pct_change().dropna()

    if close.empty:
        return {
            "total_return": 0.0,
            "annual_volatility": 0.0,
            "max_drawdown": 0.0,
            "sharpe_ratio": 0.0,
            "best_day": 0.0,
            "worst_day": 0.0,
            "average_daily_return": 0.0,
            "positive_day_ratio": 0.0,
        }

    total_return = close.iloc[-1] / close.iloc[0] - 1
    annual_volatility = returns.std() * math.sqrt(252) if not returns.empty else 0.0
    annual_return = returns.mean() * 252 if not returns.empty else 0.0
    sharpe_ratio = annual_return / annual_volatility if annual_volatility else 0.0
    drawdown = close / close.cummax() - 1

    return {
        "total_return": float(total_return),
        "annual_volatility": float(annual_volatility),
        "max_drawdown": float(drawdown.min()),
        "sharpe_ratio": float(sharpe_ratio),
        "best_day": float(returns.max()) if not returns.empty else 0.0,
        "worst_day": float(returns.min()) if not returns.empty else 0.0,
        "average_daily_return": float(returns.mean()) if not returns.empty else 0.0,
        "positive_day_ratio": float((returns > 0).mean()) if not returns.empty else 0.0,
    }


def trend_signal(data):
    latest = data.dropna(subset=["Close", "SMA20", "SMA50"]).tail(1)

    if latest.empty:
        return "Insufficient data"

    row = latest.iloc[0]

    if row["Close"] > row["SMA20"] > row["SMA50"]:
        return "Bullish"

    if row["Close"] < row["SMA20"] < row["SMA50"]:
        return "Bearish"

    return "Mixed"


def rsi_signal(latest_rsi):
    if latest_rsi is None:
        return "Insufficient data"

    if latest_rsi >= 70:
        return "Overbought"

    if latest_rsi <= 30:
        return "Oversold"

    return "Neutral"
