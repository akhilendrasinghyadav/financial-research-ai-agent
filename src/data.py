import re

import pandas as pd
import yfinance as yf


SYMBOL_PATTERN = re.compile(r"\b[A-Z0-9&-]+(?:\.NS|\.BO|\^NSEI)\b")


def normalize_symbol(symbol):
    cleaned = symbol.strip().upper()

    if not cleaned:
        return ""

    if cleaned.startswith("^") or cleaned.endswith((".NS", ".BO")):
        return cleaned

    return f"{cleaned}.NS"


def extract_stock_symbol(question):
    normalized_question = question.upper()
    match = SYMBOL_PATTERN.search(normalized_question)

    if match:
        return normalize_symbol(match.group(0))

    fallback = re.search(r"\b[A-Z]{2,12}\b", normalized_question)
    return normalize_symbol(fallback.group(0)) if fallback else None


def fetch_history(symbol, period):
    normalized_symbol = normalize_symbol(symbol)

    if not normalized_symbol:
        return pd.DataFrame()

    data = yf.Ticker(normalized_symbol).history(period=period, interval="1d")

    if data is None or data.empty or "Close" not in data.columns:
        return pd.DataFrame()

    data = data.dropna(subset=["Close"]).copy()
    data.index = pd.to_datetime(data.index)
    return data
