import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="2026 AI Master Trader", layout="wide")
st_autorefresh(interval=60000, key="master_refresh")

# 1. Asset Mapping for News & Charts
assets = {
    "GOLD": "GC=F", "BITCOIN": "BTC-USD", 
    "OIL": "BZ=F", "GBP/USD": "GBPUSD=X"
}

st.title("🛡️ 2026 AI Master Command Center")
selected_name = st.sidebar.selectbox("Select Asset to Trade", list(assets.keys()))
ticker = assets[selected_name]

# 2. Strategy & Data Engine
df = yf.download(ticker, period="60d", interval="1d")
df['Fast_MA'] = df['Close'].rolling(window=9).mean()
df['Slow_MA'] = df['Close'].rolling(window=21).mean()
df['Signal'] = (df['Fast_MA'] > df['Slow_MA']).astype(int)
df['Entry_Exit'] = df['Signal'].diff()

# 3. Layout: Chart on Left, News on Right
col_chart, col_news = st.columns([2, 1])

with col_chart:
    st.subheader(f"Interactive {selected_name} Analysis")
    fig = go.Figure(data=[go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'], name='Price')])
    
    # Entry/Exit Markers
    entries = df[df['Entry_Exit'] == 1]
    exits = df[df['Entry_Exit'] == -1]
    fig.add_trace(go.Scatter(x=entries.index, y=entries['Low']*0.98, mode='markers', marker=dict(symbol='triangle-up', size=12, color='lime'), name='ENTRY'))
    fig.add_trace(go.Scatter(x=exits.index, y=exits['High']*1.02, mode='markers', marker=dict(symbol='triangle-down', size=12, color='red'), name='EXIT'))
    
    fig.update_layout(template="plotly_dark", height=600, xaxis_rangeslider_visible=False)
    st.plotly_chart(fig, use_container_width=True)

with col_news:
    st.subheader(f"Live {selected_name} News")
    news = yf.Ticker(ticker).news
    for item in news[:5]: # Shows top 5 latest 2026 headlines
        st.write(f"**{item['title']}**")
        st.caption(f"Source: {item['publisher']} | [Link]({item['link']})")
        st.divider()

# 4. Final Status
st.info(f"**Current Strategy Status:** {'HOLDING BUY' if df['Signal'].iloc[-1] == 1 else 'WAITING FOR ENTRY'}")
