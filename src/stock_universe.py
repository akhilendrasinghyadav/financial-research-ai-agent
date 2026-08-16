import pandas as pd

DHAN_MASTER_URL = "https://images.dhan.co/api-data/api-scrip-master.csv"

FALLBACK_STOCKS = [
    {"symbol": "RELIANCE.NS", "label": "RELIANCE.NS - Reliance Industries (NSE)"},
    {"symbol": "TCS.NS", "label": "TCS.NS - Tata Consultancy Services (NSE)"},
    {"symbol": "INFY.NS", "label": "INFY.NS - Infosys (NSE)"},
    {"symbol": "HDFCBANK.NS", "label": "HDFCBANK.NS - HDFC Bank (NSE)"},
    {"symbol": "SBIN.NS", "label": "SBIN.NS - State Bank of India (NSE)"},
]


def _find_column(df, names):
    lookup = {column.upper(): column for column in df.columns}
    for name in names:
        if name.upper() in lookup:
            return lookup[name.upper()]
    return None


def _clean(value):
    if pd.isna(value):
        return ""
    return str(value).strip()


def load_indian_stock_options():
    try:
        df = pd.read_csv(DHAN_MASTER_URL, low_memory=False)
    except Exception:
        return FALLBACK_STOCKS

    exchange_col = _find_column(df, ["EXCH_ID", "SEM_EXM_EXCH_ID"])
    instrument_col = _find_column(df, ["INSTRUMENT_NAME", "SEM_INSTRUMENT_NAME"])
    trading_col = _find_column(df, ["TRADING_SYMBOL", "SEM_TRADING_SYMBOL", "SYMBOL_NAME"])
    security_id_col = _find_column(df, ["SECURITY_ID", "SEM_SMST_SECURITY_ID"])
    name_col = _find_column(df, ["CUSTOM_SYMBOL", "SM_CUSTOM_SYMBOL", "SYMBOL_NAME"])

    if not exchange_col or not trading_col:
        return FALLBACK_STOCKS

    options = {}

    for _, row in df.iterrows():
        exchange = _clean(row.get(exchange_col)).upper()
        instrument = _clean(row.get(instrument_col)).upper() if instrument_col else ""

        if exchange not in {"NSE", "BSE"}:
            continue

        if instrument and "EQUITY" not in instrument:
            continue

        trading_symbol = _clean(row.get(trading_col)).upper()
        security_id = _clean(row.get(security_id_col)) if security_id_col else ""
        company_name = _clean(row.get(name_col)) if name_col else trading_symbol

        if not trading_symbol:
            continue

        if exchange == "NSE":
            yahoo_symbol = f"{trading_symbol}.NS"
        else:
            yahoo_symbol = f"{security_id}.BO" if security_id.isdigit() else f"{trading_symbol}.BO"

        options[yahoo_symbol] = {
            "symbol": yahoo_symbol,
            "label": f"{yahoo_symbol} - {company_name} ({exchange})",
        }

    return sorted(options.values(), key=lambda item: item["label"]) or FALLBACK_STOCKS