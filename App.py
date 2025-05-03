import streamlit as st
import requests
import pandas as pd
from babel.numbers import format_currency

# Konfigurasi halaman
st.set_page_config(page_title="Bloomberg Crypto Lite", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
        body { background-color: #0e1117; color: #fafafa; }
        .stDataFrame { background-color: #0e1117; }
        .css-18e3th9 { background-color: #0e1117; }
    </style>
""", unsafe_allow_html=True)

# CoinMarketCap API KEY (pakai yang kamu berikan)
CMC_API_KEY = "3d6ac872-bdf1-482c-abfe-541be50b59f5"

# Fungsi ambil kurs USD ke IDR
@st.cache_data(ttl=3600)
def get_usd_to_idr():
    url = "https://api.exchangerate.host/latest?base=USD&symbols=IDR"
    res = requests.get(url).json()
    if "rates" in res and "IDR" in res["rates"]:
        return res["rates"]["IDR"]
    else:
        return 15500  # fallback

usd_to_idr = get_usd_to_idr()

# Fungsi ambil top 50 koin
@st.cache_data(ttl=600)
def fetch_top_cryptos():
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
    headers = {"X-CMC_PRO_API_KEY": CMC_API_KEY}
    params = {"start": "1", "limit": "50", "convert": "USD"}
    response = requests.get(url, headers=headers, params=params).json()
    return response["data"]

data = fetch_top_cryptos()

# Tampilkan tabel
st.title("Bloomberg Crypto Lite - Modul 1: Dashboard")

rows = []
for coin in data:
    name = coin["name"]
    symbol = coin["symbol"]
    price_usd = coin["quote"]["USD"]["price"]
    price_idr = price_usd * usd_to_idr
    pct_24h = coin["quote"]["USD"]["percent_change_24h"]
    status = "Bullish" if pct_24h > 0 else "Bearish"

    rows.append({
        "Name": name,
        "Symbol": symbol,
        "Price (USD)": format_currency(price_usd, 'USD', locale='en_US'),
        "Price (IDR)": format_currency(price_idr, 'IDR', locale='id_ID'),
        "24h %": round(pct_24h, 2),
        "Status": status
    })

df = pd.DataFrame(rows)
st.dataframe(df, use_container_width=True)
