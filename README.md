# Financial Research AI Agent

A Streamlit-based financial research assistant for Indian stock market analysis.

## Week 1-2 Features

- Indian stock lookup using Yahoo Finance symbols such as `RELIANCE.NS`, `TCS.NS`, and `INFY.NS`
- Candlestick price chart
- 20-day moving average
- RSI indicator
- Stock comparison chart
- Educational disclaimer for financial analysis

## Tech Stack

- Python
- Streamlit
- yfinance
- Plotly
- pandas / numpy

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Run Locally

```bash
python -m streamlit run app.py
```

Then open the local Streamlit URL shown in the terminal.

## Example Symbols

- `RELIANCE.NS`
- `TCS.NS`
- `INFY.NS`
- `HDFCBANK.NS`
- `SBIN.NS`

## Deployment

This project is ready for Streamlit Community Cloud deployment.

1. Push this folder to GitHub.
2. Open Streamlit Community Cloud.
3. Create a new app from the GitHub repository.
4. Select `app.py` as the entry file.
5. Deploy.

## Live Demo

Streamlit App: https://financial-research-ai-agent-lj5i2bxh7tj6csoia6ga4t.streamlit.app/

## Demo Video

Demo video is included with the final submission.

## Disclaimer

This app provides educational financial analysis only. It does not provide investment advice. Consult a registered financial advisor before making investment decisions.
