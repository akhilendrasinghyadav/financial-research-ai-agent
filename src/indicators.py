import numpy as np


def calculate_rsi(close_prices, window=14):
    delta = close_prices.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(window=window, min_periods=window).mean()
    avg_loss = loss.rolling(window=window, min_periods=window).mean()
    rs = avg_gain / avg_loss.replace(0, np.nan)
    return 100 - (100 / (1 + rs))


def add_indicators(data):
    enriched = data.copy()
    close = enriched["Close"]

    enriched["Daily Return"] = close.pct_change()
    enriched["SMA20"] = close.rolling(window=20, min_periods=1).mean()
    enriched["SMA50"] = close.rolling(window=50, min_periods=1).mean()
    enriched["EMA20"] = close.ewm(span=20, adjust=False).mean()

    rolling_std = close.rolling(window=20, min_periods=1).std()
    enriched["BB_UPPER"] = enriched["SMA20"] + 2 * rolling_std
    enriched["BB_LOWER"] = enriched["SMA20"] - 2 * rolling_std
    enriched["RSI"] = calculate_rsi(close)

    ema12 = close.ewm(span=12, adjust=False).mean()
    ema26 = close.ewm(span=26, adjust=False).mean()
    enriched["MACD"] = ema12 - ema26
    enriched["MACD_SIGNAL"] = enriched["MACD"].ewm(span=9, adjust=False).mean()
    enriched["MACD_HIST"] = enriched["MACD"] - enriched["MACD_SIGNAL"]

    return enriched
