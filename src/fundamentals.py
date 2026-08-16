import yfinance as yf


def format_large_number(value):
    if value is None:
        return "N/A"

    try:
        value = float(value)
    except (TypeError, ValueError):
        return "N/A"

    if value >= 1_00_00_00_000:
        return f"INR {value / 1_00_00_00_000:.2f} Cr"

    return f"INR {value:,.0f}"


def format_percent(value):
    if value is None:
        return "N/A"

    try:
        return f"{value * 100:.2f}%"
    except (TypeError, ValueError):
        return "N/A"

def calculate_fundamental_score(info):
    score = 0
    reasons = []

    pe_ratio = info.get("trailingPE")
    debt_equity = info.get("debtToEquity")
    profit_margin = info.get("profitMargins")
    revenue_growth = info.get("revenueGrowth")

    if pe_ratio and pe_ratio < 30:
        score += 1
        reasons.append("reasonable P/E")

    if debt_equity and debt_equity < 100:
        score += 1
        reasons.append("manageable debt")

    if profit_margin and profit_margin > 0.10:
        score += 1
        reasons.append("good profit margin")

    if revenue_growth and revenue_growth > 0:
        score += 1
        reasons.append("positive revenue growth")

    if score >= 3:
        label = "Strong"
    elif score == 2:
        label = "Average"
    else:
        label = "Weak"

    return label, ", ".join(reasons) if reasons else "Limited or weak fundamentals"
def fetch_fundamentals(symbol):
    try:
        info = yf.Ticker(symbol).info
    except Exception:
        return {}

    if not info or not any(info.get(key) for key in ["longName", "marketCap", "sector", "trailingPE"]):
        return {}

    score_label, score_reason = calculate_fundamental_score(info)

    return {
        "Company": info.get("longName", symbol),
        "Sector": info.get("sector", "N/A"),
        "Industry": info.get("industry", "N/A"),
        "Market Cap": format_large_number(info.get("marketCap")),
        "P/E Ratio": info.get("trailingPE", "N/A"),
        "Debt/Equity": info.get("debtToEquity", "N/A"),
        "Profit Margin": format_percent(info.get("profitMargins")),
        "Revenue Growth": format_percent(info.get("revenueGrowth")),
        "Dividend Yield": format_percent(info.get("dividendYield")),
        "Fundamental Score": score_label,
        "Score Reason": score_reason,
    }
