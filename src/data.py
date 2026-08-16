import re

import pandas as pd
import yfinance as yf


SYMBOL_PATTERN = re.compile(r"\^NSEI|\b[A-Z0-9&-]+(?:\.(?:NS|BO))?\b")


def normalize_symbol(symbol):
    cleaned = symbol.strip().upper().replace(" ", "")

    if not cleaned:
        return ""

    if cleaned.startswith("^"):
        return cleaned

    if cleaned.endswith((".NS", ".BO")):
        return cleaned

    return f"{cleaned}.NS"


def extract_stock_symbol(question):
    normalized_question = question.upper()

    explicit_match = re.search(r"\b[A-Z0-9&-]+(?:\.(?:NS|BO))\b|\^NSEI", normalized_question)
    if explicit_match:
        return normalize_symbol(explicit_match.group(0))

    stop_words = {
        "WHAT", "IS", "THE", "LATEST", "PRICE", "OF", "SHOW", "ME",
        "TELL", "ABOUT", "STOCK", "SHARE", "FOR"
    }

    candidates = re.findall(r"\b[A-Z0-9&-]{2,12}\b", normalized_question)

    for candidate in candidates:
        if candidate not in stop_words:
            return normalize_symbol(candidate)

    return None


def fetch_history(symbol, period):
    normalized_symbol = normalize_symbol(symbol)

    if not normalized_symbol:
        return pd.DataFrame()

    if period == "1d":
     interval = "1m"
    elif period == "5d":
     interval = "5m"
    else:
     interval = "1d"

    data = yf.Ticker(normalized_symbol).history(period=period, interval=interval)
    if data is None or data.empty or "Close" not in data.columns:
        return pd.DataFrame()

    data = data.dropna(subset=["Close"]).copy()
    data.index = pd.to_datetime(data.index)
    return data
