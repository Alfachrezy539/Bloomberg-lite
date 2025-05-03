import streamlit as st
import requests
import pandas as pd
from babel.numbers import format_currency

st.set_page_config(page_title="Crypto Bloomberg - Real-time Dashboard", layout="wide")

API_KEY = "3d6ac872-bdf1-482c-abfe-541be50b59f5"
headers = {"X-CMC_PRO_API_KEY": API_KEY}

@st.cache_data(ttl=600)
def get_usd_to_idr():
    url = "https://api.exchangerate.host/latest?base=USD"
    res = requests.get(url).json()
    return res["rates"]["IDR"]

@st.cache_data(ttl=300)
def get_top_50_coins():
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
    params = {
        "start": "1",
        "limit": "50",
        "convert": "USD"
    }
    res = requests.get(url, headers=headers, params=params).json()
    return res["data"]

# Title
st.title("Crypto Dashboard - Top 50 Coins (USD & IDR)")
usd_to_idr = get_usd_to_idr()
data = get_top_50_coins()

# Tabel
rows = []
for coin in data:
    price_usd = coin["quote"]["USD"]["price"]
    price_idr = price_usd * usd_to_idr
    rows.append({
        "Name": coin["name"],
        "Symbol": coin["symbol"],
        "Price (USD)": format_currency(price_usd, 'USD', locale='en_US'),
        "Price (IDR)": format_currency(price_idr, 'IDR', locale='id_ID'),
        "1h %": coin["quote"]["USD"]["percent_change_1h"],
        "24h %": coin["quote"]["USD"]["percent_change_24h"],
        "7d %": coin["quote"]["USD"]["percent_change_7d"],
        "Volume 24h": f'{coin["quote"]["USD"]["volume_24h"] / 1e6:.2f}M',
        "Market Cap": f'{coin["quote"]["USD"]["market_cap"] / 1e9:.2f}B'
    })

df = pd.DataFrame(rows)
st.dataframe(df, use_container_width=True)
