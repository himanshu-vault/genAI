import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings("ignore")

st.set_page_config(
    page_title="StockSense India",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Styling ──────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

.stApp { background: #0d0f14; }

/* Sidebar */
[data-testid="stSidebar"] {
    background: #13151c !important;
    border-right: 1px solid #1e2130;
}
[data-testid="stSidebar"] * { color: #c8cad4 !important; }

/* Metric cards */
.metric-card {
    background: #13151c;
    border: 1px solid #1e2130;
    border-radius: 12px;
    padding: 18px 22px;
    transition: border-color 0.2s;
}
.metric-card:hover { border-color: #3a3f5c; }
.metric-label { font-size: 11px; letter-spacing: 0.08em; text-transform: uppercase; color: #6b7280; margin-bottom: 6px; }
.metric-value { font-family: 'Space Mono', monospace; font-size: 26px; font-weight: 700; color: #e8eaf0; }
.metric-sub { font-size: 12px; margin-top: 4px; }

/* Signal badge */
.signal-buy  { background:#0d2b1f; border:1px solid #1a5c3a; color:#4ade80; padding:6px 16px; border-radius:6px; font-family:'Space Mono',monospace; font-size:13px; font-weight:700; letter-spacing:0.05em; }
.signal-sell { background:#2b0d0d; border:1px solid #5c1a1a; color:#f87171; padding:6px 16px; border-radius:6px; font-family:'Space Mono',monospace; font-size:13px; font-weight:700; letter-spacing:0.05em; }
.signal-hold { background:#1e1f0d; border:1px solid #4a4c1a; color:#facc15; padding:6px 16px; border-radius:6px; font-family:'Space Mono',monospace; font-size:13px; font-weight:700; letter-spacing:0.05em; }

/* Section headers */
.section-header { font-family:'Space Mono',monospace; font-size:11px; letter-spacing:0.15em; text-transform:uppercase; color:#4b5563; margin: 24px 0 12px; border-bottom:1px solid #1e2130; padding-bottom:8px; }

/* Indicator row */
.ind-row { display:flex; justify-content:space-between; align-items:center; padding:10px 0; border-bottom:1px solid #1a1c24; }
.ind-name { font-size:13px; color:#9ca3af; }
.ind-val  { font-family:'Space Mono',monospace; font-size:13px; color:#e8eaf0; }
.ind-bull { color:#4ade80; font-size:11px; font-weight:600; }
.ind-bear { color:#f87171; font-size:11px; font-weight:600; }
.ind-neut { color:#facc15; font-size:11px; font-weight:600; }

/* Override streamlit defaults */
.stSelectbox label, .stSlider label, .stTextInput label { color: #9ca3af !important; font-size: 12px !important; letter-spacing: 0.05em; }
div[data-baseweb="select"] { background: #1a1c24 !important; border-color: #2a2d3e !important; }
.stButton > button {
    background: #1e4d8c; border: none; color: white; font-family: 'Space Mono', monospace;
    font-size: 12px; letter-spacing: 0.05em; border-radius: 8px; padding: 10px 20px;
    transition: background 0.2s;
}
.stButton > button:hover { background: #2563b0; }
h1, h2, h3 { color: #e8eaf0 !important; }
p, li { color: #9ca3af; }
.stDataFrame { background: #13151c; }
</style>
""", unsafe_allow_html=True)


# ── Constants ─────────────────────────────────────────────────────────────────
NSE_STOCKS = {
    "Reliance Industries": "RELIANCE.NS",
    "TCS": "TCS.NS",
    "HDFC Bank": "HDFCBANK.NS",
    "Infosys": "INFY.NS",
    "ICICI Bank": "ICICIBANK.NS",
    "Hindustan Unilever": "HINDUNILVR.NS",
    "Bajaj Finance": "BAJFINANCE.NS",
    "Kotak Mahindra Bank": "KOTAKBANK.NS",
    "State Bank of India": "SBIN.NS",
    "Wipro": "WIPRO.NS",
    "Maruti Suzuki": "MARUTI.NS",
    "Asian Paints": "ASIANPAINT.NS",
    "ITC": "ITC.NS",
    "Titan Company": "TITAN.NS",
    "Larsen & Toubro": "LT.NS",
    "Sun Pharma": "SUNPHARMA.NS",
    "Axis Bank": "AXISBANK.NS",
    "Tata Motors": "TATAMOTORS.NS",
    "Tata Steel": "TATASTEEL.NS",
    "NTPC": "NTPC.NS",
    "Nifty 50 Index": "^NSEI",
    "Bank Nifty": "^NSEBANK",
}

PERIODS = {"1 Month": "1mo", "3 Months": "3mo", "6 Months": "6mo", "1 Year": "1y", "2 Years": "2y"}


# ── Signal Logic ──────────────────────────────────────────────────────────────
def compute_indicators(df):
    close = df["Close"]
    high  = df["High"]
    low   = df["Low"]

    # RSI
    delta = close.diff()
    gain  = delta.clip(lower=0).rolling(14).mean()
    loss  = (-delta.clip(upper=0)).rolling(14).mean()
    rs    = gain / loss
    df["RSI"] = 100 - (100 / (1 + rs))

    # MACD
    ema12 = close.ewm(span=12).mean()
    ema26 = close.ewm(span=26).mean()
    df["MACD"]        = ema12 - ema26
    df["MACD_Signal"] = df["MACD"].ewm(span=9).mean()
    df["MACD_Hist"]   = df["MACD"] - df["MACD_Signal"]

    # Bollinger Bands
    sma20 = close.rolling(20).mean()
    std20 = close.rolling(20).std()
    df["BB_Upper"] = sma20 + 2 * std20
    df["BB_Lower"] = sma20 - 2 * std20
    df["BB_Mid"]   = sma20

    # EMA
    df["EMA20"] = close.ewm(span=20).mean()
    df["EMA50"] = close.ewm(span=50).mean()

    # ATR
    tr = pd.concat([
        high - low,
        (high - close.shift()).abs(),
        (low  - close.shift()).abs()
    ], axis=1).max(axis=1)
    df["ATR"] = tr.rolling(14).mean()

    # Volume MA
    df["Vol_MA20"] = df["Volume"].rolling(20).mean()

    return df


def generate_signal(df):
    latest  = df.iloc[-1]
    prev    = df.iloc[-2]
    signals = []
    score   = 0

    rsi = latest["RSI"]
    if rsi < 35:
        signals.append(("RSI", f"{rsi:.1f}", "Oversold → bullish", "bull"))
        score += 2
    elif rsi > 65:
        signals.append(("RSI", f"{rsi:.1f}", "Overbought → bearish", "bear"))
        score -= 2
    else:
        signals.append(("RSI", f"{rsi:.1f}", "Neutral", "neut"))

    # MACD crossover
    if latest["MACD"] > latest["MACD_Signal"] and prev["MACD"] <= prev["MACD_Signal"]:
        signals.append(("MACD", "Crossover ↑", "Bullish crossover", "bull"))
        score += 3
    elif latest["MACD"] < latest["MACD_Signal"] and prev["MACD"] >= prev["MACD_Signal"]:
        signals.append(("MACD", "Crossover ↓", "Bearish crossover", "bear"))
        score -= 3
    elif latest["MACD"] > latest["MACD_Signal"]:
        signals.append(("MACD", f"{latest['MACD']:.2f}", "Above signal → bullish", "bull"))
        score += 1
    else:
        signals.append(("MACD", f"{latest['MACD']:.2f}", "Below signal → bearish", "bear"))
        score -= 1

    # Bollinger Band position
    close = latest["Close"]
    bb_pos = (close - latest["BB_Lower"]) / (latest["BB_Upper"] - latest["BB_Lower"]) * 100
    if bb_pos < 15:
        signals.append(("Bollinger", f"{bb_pos:.0f}%", "Near lower band → potential bounce", "bull"))
        score += 2
    elif bb_pos > 85:
        signals.append(("Bollinger", f"{bb_pos:.0f}%", "Near upper band → potential reversal", "bear"))
        score -= 2
    else:
        signals.append(("Bollinger", f"{bb_pos:.0f}%", "Mid-band zone", "neut"))

    # EMA trend
    if latest["EMA20"] > latest["EMA50"]:
        signals.append(("EMA 20/50", f"↑ Uptrend", "Price above both EMAs", "bull"))
        score += 2
    else:
        signals.append(("EMA 20/50", f"↓ Downtrend", "Price below EMA50", "bear"))
        score -= 2

    # Volume confirmation
    if latest["Volume"] > latest["Vol_MA20"] * 1.3:
        signals.append(("Volume", f"{latest['Volume']/latest['Vol_MA20']:.1f}x avg", "High volume confirmation", "bull" if score > 0 else "bear"))
        score += 1 if score > 0 else -1
    else:
        signals.append(("Volume", f"{latest['Volume']/latest['Vol_MA20']:.1f}x avg", "Average volume", "neut"))

    # Final verdict
    if score >= 4:
        verdict = "BUY"
    elif score <= -4:
        verdict = "SELL"
    else:
        verdict = "HOLD"

    return verdict, score, signals


def support_resistance(df, n=5):
    """Simple S/R using rolling min/max pivots"""
    close   = df["Close"]
    recent  = df.tail(60)
    highs   = recent["High"].nlargest(n).values
    lows    = recent["Low"].nsmallest(n).values
    return sorted(lows, reverse=True), sorted(highs, reverse=True)


# ── Main UI ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📈 StockSense India")
    st.markdown("<div style='font-size:11px;color:#4b5563;margin-bottom:20px;'>Technical Signal Scanner</div>", unsafe_allow_html=True)

    stock_name = st.selectbox("Stock / Index", list(NSE_STOCKS.keys()), index=0)
    period_label = st.selectbox("Analysis Period", list(PERIODS.keys()), index=3)

    st.markdown("---")
    st.markdown("<div style='font-size:11px;color:#4b5563;'>Custom NSE Symbol</div>", unsafe_allow_html=True)
    custom_sym = st.text_input("e.g. ZOMATO.NS", value="", placeholder="SYMBOL.NS")

    run = st.button("🔍  Analyse", use_container_width=True)

    st.markdown("---")
    st.markdown("""
    <div style='font-size:11px;color:#4b5563;line-height:1.8;'>
    <b style='color:#6b7280;'>Indicators used</b><br>
    RSI (14) · MACD (12,26,9)<br>
    Bollinger Bands (20,2)<br>
    EMA 20 / EMA 50<br>
    ATR (14) · Volume MA<br><br>
    <b style='color:#6b7280;'>Disclaimer</b><br>
    For educational use only.<br>
    Not financial advice.
    </div>
    """, unsafe_allow_html=True)


# ── Ticker Resolution ──────────────────────────────────────────────────────────
if custom_sym.strip():
    ticker_sym  = custom_sym.strip().upper()
    ticker_name = ticker_sym
else:
    ticker_sym  = NSE_STOCKS[stock_name]
    ticker_name = stock_name

period = PERIODS[period_label]


# ── Load & Process ─────────────────────────────────────────────────────────────
@st.cache_data(ttl=300)
def load_data(sym, period):
    df = yf.download(sym, period=period, progress=False, auto_adjust=True)
    if df.empty:
        return None
    df.columns = [c[0] if isinstance(c, tuple) else c for c in df.columns]
    df = df.dropna()
    return compute_indicators(df)


if run or "df_cache" not in st.session_state:
    with st.spinner("Fetching data from Yahoo Finance…"):
        df = load_data(ticker_sym, period)
    if df is None or len(df) < 30:
        st.error("Could not fetch data. Check the symbol and try again.")
        st.stop()
    st.session_state["df_cache"]   = df
    st.session_state["ticker_name"] = ticker_name
    st.session_state["ticker_sym"]  = ticker_sym
else:
    df          = st.session_state["df_cache"]
    ticker_name = st.session_state["ticker_name"]
    ticker_sym  = st.session_state["ticker_sym"]


# ── Compute ────────────────────────────────────────────────────────────────────
verdict, score, signals = generate_signal(df)
latest   = df.iloc[-1]
prev_day = df.iloc[-2]
supports, resistances = support_resistance(df)

price_chg     = latest["Close"] - prev_day["Close"]
price_chg_pct = price_chg / prev_day["Close"] * 100
period_start  = df.iloc[0]["Close"]
period_ret    = (latest["Close"] - period_start) / period_start * 100


# ── Header ─────────────────────────────────────────────────────────────────────
col_title, col_badge = st.columns([3, 1])
with col_title:
    st.markdown(f"<h1 style='margin-bottom:2px;font-family:Space Mono,monospace;font-size:28px;'>{ticker_name}</h1>", unsafe_allow_html=True)
    st.markdown(f"<div style='color:#4b5563;font-family:Space Mono,monospace;font-size:12px;'>{ticker_sym} · NSE · Data via Yahoo Finance</div>", unsafe_allow_html=True)
with col_badge:
    badge_class = {"BUY": "signal-buy", "SELL": "signal-sell", "HOLD": "signal-hold"}[verdict]
    emoji = {"BUY": "▲", "SELL": "▼", "HOLD": "◆"}[verdict]
    st.markdown(f"<div style='text-align:right;margin-top:12px;'><span class='{badge_class}'>{emoji} {verdict}</span></div>", unsafe_allow_html=True)
    st.markdown(f"<div style='text-align:right;font-size:11px;color:#4b5563;margin-top:6px;font-family:Space Mono,monospace;'>Signal score: {score:+d}/10</div>", unsafe_allow_html=True)

st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

# ── Metric Cards ──────────────────────────────────────────────────────────────
c1, c2, c3, c4, c5 = st.columns(5)
def metric_card(col, label, value, sub, sub_color="#9ca3af"):
    col.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-sub" style="color:{sub_color}">{sub}</div>
    </div>
    """, unsafe_allow_html=True)

chg_color = "#4ade80" if price_chg >= 0 else "#f87171"
ret_color = "#4ade80" if period_ret >= 0 else "#f87171"

metric_card(c1, "LTP", f"₹{latest['Close']:.2f}", f"{price_chg:+.2f} ({price_chg_pct:+.2f}%)", chg_color)
metric_card(c2, "RSI (14)", f"{latest['RSI']:.1f}", "Oversold <35  |  Overbought >65")
metric_card(c3, "ATR (14)", f"₹{latest['ATR']:.2f}", "Average True Range (volatility)")
metric_card(c4, f"{period_label} Return", f"{period_ret:+.1f}%", f"From ₹{period_start:.2f}", ret_color)
metric_card(c5, "Volume", f"{latest['Volume']/1e5:.1f}L", f"Avg: {latest['Vol_MA20']/1e5:.1f}L")

st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

# ── Chart ──────────────────────────────────────────────────────────────────────
fig = make_subplots(
    rows=3, cols=1,
    shared_xaxes=True,
    row_heights=[0.55, 0.25, 0.20],
    vertical_spacing=0.02,
)

# Candlestick
fig.add_trace(go.Candlestick(
    x=df.index, open=df["Open"], high=df["High"], low=df["Low"], close=df["Close"],
    increasing_fillcolor="#1a5c3a", increasing_line_color="#4ade80",
    decreasing_fillcolor="#5c1a1a", decreasing_line_color="#f87171",
    name="Price", showlegend=False
), row=1, col=1)

# EMAs
fig.add_trace(go.Scatter(x=df.index, y=df["EMA20"], line=dict(color="#60a5fa", width=1.2), name="EMA 20"), row=1, col=1)
fig.add_trace(go.Scatter(x=df.index, y=df["EMA50"], line=dict(color="#f59e0b", width=1.2), name="EMA 50"), row=1, col=1)

# Bollinger Bands
fig.add_trace(go.Scatter(x=df.index, y=df["BB_Upper"], line=dict(color="#6366f1", width=0.8, dash="dash"), name="BB Upper", showlegend=False), row=1, col=1)
fig.add_trace(go.Scatter(x=df.index, y=df["BB_Lower"], line=dict(color="#6366f1", width=0.8, dash="dash"), name="BB Lower",
    fill="tonexty", fillcolor="rgba(99,102,241,0.06)", showlegend=False), row=1, col=1)

# Support / Resistance lines
for s in supports[:2]:
    fig.add_hline(y=s, line_dash="dot", line_color="#4ade80", line_width=0.8, opacity=0.4, row=1, col=1)
for r in resistances[:2]:
    fig.add_hline(y=r, line_dash="dot", line_color="#f87171", line_width=0.8, opacity=0.4, row=1, col=1)

# MACD
colors_hist = ["#4ade80" if v >= 0 else "#f87171" for v in df["MACD_Hist"]]
fig.add_trace(go.Bar(x=df.index, y=df["MACD_Hist"], marker_color=colors_hist, name="MACD Hist", showlegend=False), row=2, col=1)
fig.add_trace(go.Scatter(x=df.index, y=df["MACD"], line=dict(color="#60a5fa", width=1), name="MACD"), row=2, col=1)
fig.add_trace(go.Scatter(x=df.index, y=df["MACD_Signal"], line=dict(color="#f59e0b", width=1), name="Signal"), row=2, col=1)

# RSI
fig.add_trace(go.Scatter(x=df.index, y=df["RSI"], line=dict(color="#a78bfa", width=1.5), name="RSI", showlegend=False), row=3, col=1)
fig.add_hline(y=70, line_dash="dot", line_color="#f87171", line_width=0.8, opacity=0.5, row=3, col=1)
fig.add_hline(y=30, line_dash="dot", line_color="#4ade80", line_width=0.8, opacity=0.5, row=3, col=1)

fig.update_layout(
    paper_bgcolor="#0d0f14",
    plot_bgcolor="#0d0f14",
    font=dict(family="DM Sans", size=12, color="#9ca3af"),
    height=580,
    margin=dict(l=0, r=0, t=10, b=0),
    legend=dict(orientation="h", y=1.01, x=0, font=dict(size=11), bgcolor="rgba(0,0,0,0)"),
    xaxis_rangeslider_visible=False,
    xaxis3=dict(showgrid=False, zeroline=False, color="#4b5563"),
    yaxis=dict(gridcolor="#1a1c24", zeroline=False, tickformat=",.0f", tickprefix="₹"),
    yaxis2=dict(gridcolor="#1a1c24", zeroline=False),
    yaxis3=dict(gridcolor="#1a1c24", zeroline=False, range=[0, 100]),
)
for i in range(1, 4):
    fig.update_xaxes(showgrid=False, zeroline=False, color="#4b5563", row=i, col=1)

st.plotly_chart(fig, use_container_width=True)


# ── Bottom Section ─────────────────────────────────────────────────────────────
left, right = st.columns([1, 1])

with left:
    st.markdown("<div class='section-header'>Indicator Breakdown</div>", unsafe_allow_html=True)
    for name, value, reason, direction in signals:
        dir_label = {"bull": '<span class="ind-bull">▲ Bullish</span>',
                     "bear": '<span class="ind-bear">▼ Bearish</span>',
                     "neut": '<span class="ind-neut">◆ Neutral</span>'}[direction]
        st.markdown(f"""
        <div class="ind-row">
            <div>
                <div class="ind-name">{name}</div>
                <div style="font-size:11px;color:#4b5563;margin-top:2px;">{reason}</div>
            </div>
            <div style="text-align:right;">
                <div class="ind-val">{value}</div>
                <div style="margin-top:2px;">{dir_label}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

with right:
    st.markdown("<div class='section-header'>Key Levels</div>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class="ind-row">
        <div class="ind-name">Current Price</div>
        <div class="ind-val">₹{latest['Close']:.2f}</div>
    </div>
    """, unsafe_allow_html=True)
    for i, r in enumerate(resistances[:3], 1):
        st.markdown(f"""
        <div class="ind-row">
            <div class="ind-name">Resistance R{i}</div>
            <div><span class="ind-val">₹{r:.2f}</span> <span class="ind-bear" style="font-size:10px;margin-left:8px;">+{(r-latest['Close'])/latest['Close']*100:.1f}%</span></div>
        </div>
        """, unsafe_allow_html=True)
    for i, s in enumerate(supports[:3], 1):
        st.markdown(f"""
        <div class="ind-row">
            <div class="ind-name">Support S{i}</div>
            <div><span class="ind-val">₹{s:.2f}</span> <span class="ind-bull" style="font-size:10px;margin-left:8px;">{(s-latest['Close'])/latest['Close']*100:.1f}%</span></div>
        </div>
        """, unsafe_allow_html=True)

    # Suggested stop-loss & target
    atr = latest["ATR"]
    if verdict == "BUY":
        sl      = latest["Close"] - 1.5 * atr
        target1 = latest["Close"] + 2.0 * atr
        target2 = latest["Close"] + 3.5 * atr
    else:
        sl      = latest["Close"] + 1.5 * atr
        target1 = latest["Close"] - 2.0 * atr
        target2 = latest["Close"] - 3.5 * atr

    st.markdown("<div class='section-header' style='margin-top:20px;'>ATR-Based Levels (1.5× ATR)</div>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class="ind-row">
        <div class="ind-name">Stop Loss</div>
        <div class="ind-val" style="color:#f87171;">₹{sl:.2f}</div>
    </div>
    <div class="ind-row">
        <div class="ind-name">Target 1 (2× ATR)</div>
        <div class="ind-val" style="color:#4ade80;">₹{target1:.2f}</div>
    </div>
    <div class="ind-row">
        <div class="ind-name">Target 2 (3.5× ATR)</div>
        <div class="ind-val" style="color:#4ade80;">₹{target2:.2f}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height:30px'></div>", unsafe_allow_html=True)
st.markdown("<div style='text-align:center;font-size:11px;color:#374151;'>StockSense India MVP · Data via Yahoo Finance · Not financial advice · For educational use only</div>", unsafe_allow_html=True)