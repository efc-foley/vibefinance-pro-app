import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta

# Page Configuration
st.set_page_config(
    page_title="VibeFinance Pro",
    page_icon="�",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Hybrid Aesthetic CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&family=Roboto:wght@400;500;700&display=swap');
    
    /* Global Styles */
    [data-testid="stAppViewContainer"] {
        background-color: #0d1117 !important;
        color: #f0f6fc !important;
    }

    [data-testid="stHeader"] {
        background: rgba(0,0,0,0);
    }

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Vibe Pro Header Styling */
    .header-container {
        padding: 3rem 0;
        text-align: center;
        background: rgba(255, 255, 255, 0.03);
        border-radius: 24px;
        margin-bottom: 2.5rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(12px);
    }

    /* Vibe Pro Search & Button Styling */
    .stTextInput > div > div > input {
        background: rgba(15, 23, 42, 0.8) !important;
        color: #38bdf8 !important;
        border-radius: 14px !important;
        border: 2px solid rgba(56, 189, 248, 0.3) !important;
        padding: 14px 24px !important;
        font-size: 1.3rem !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    }

    .stButton > button {
        background: linear-gradient(135deg, #38bdf8 0%, #0284c7 100%) !important;
        color: white !important;
        border-radius: 14px !important;
        border: none !important;
        padding: 0.6rem 2rem !important;
        font-weight: 700 !important;
        height: 60px !important;
        width: 100% !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(56, 189, 248, 0.3) !important;
    }

    /* Yahoo Specific Dashboard Styling (For Below Search) */
    .yh-company-name {
        font-size: 2.25rem;
        font-weight: 700;
        margin: 0;
        color: #ffffff;
        font-family: 'Roboto', sans-serif;
    }
    
    .yh-price-container {
        display: flex;
        align-items: baseline;
        gap: 12px;
        margin-top: 0.5rem;
    }
    
    .yh-current-price {
        font-size: 2.5rem;
        font-weight: 700;
        color: #ffffff;
    }
    
    .yh-delta-pos { color: #00ff73; font-size: 1.25rem; font-weight: 500; }
    .yh-delta-neg { color: #ff333a; font-size: 1.25rem; font-weight: 500; }

    /* Metric Card Styling - Flatter Look */
    div[data-testid="metric-container"] {
        background: transparent;
        padding: 0;
        border: none;
    }

    div[data-testid="stMetricLabel"] > div {
        color: #8b949e !important;
        font-size: 0.85rem !important;
    }

    div[data-testid="stMetricValue"] > div {
        color: #ffffff !important;
        font-size: 1.2rem !important;
        font-weight: 600 !important;
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        border-bottom: 1px solid #30363d;
        margin-bottom: 1.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: #8b949e !important;
        font-weight: 500 !important;
    }
    
    .stTabs [aria-selected="true"] {
        color: #ffffff !important;
        border-bottom-color: #ffffff !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Centered Website Title
st.markdown("""
    <div class="header-container">
        <h1 style='font-size: 3rem; margin-bottom: 0;'>VibeFinance <span style='color: #00ff73;'>Pro</span></h1>
        <p style='color: #94a3b8;'>Advanced market intelligence with a premium aesthetic.</p>
    </div>
    """, unsafe_allow_html=True)

# Centered Search Area
col_a, col_b, col_c = st.columns([1, 2, 1])
with col_b:
    search_col, btn_col = st.columns([4, 1])
    with search_col:
        ticker_input = st.text_input("Search Ticker", placeholder="Search for symbols (e.g. NVDA)", label_visibility="collapsed").upper()
    with btn_col:
        go_btn = st.button("Go")

# Logic to handle both enter and button click
if 'ticker' not in st.session_state:
    st.session_state.ticker = "AAPL"
if ticker_input:
    st.session_state.ticker = ticker_input
ticker_symbol = st.session_state.ticker

if ticker_symbol:
    try:
        # Fetch Data
        ticker = yf.Ticker(ticker_symbol)
        info = ticker.info
        
        # Validation Check
        if not info or ('regularMarketPrice' not in info and 'currentPrice' not in info):
            st.error(f"❌ Ticker '{ticker_symbol}' not found.")
        else:
            # Header Info
            company_name = info.get('longName', ticker_symbol)
            curr_price = info.get('currentPrice') or info.get('regularMarketPrice') or info.get('navPrice')
            prev_close = info.get('previousClose') or info.get('regularMarketPreviousClose')
            
            # Custom Yahoo Header
            if curr_price and prev_close:
                price_change = curr_price - prev_close
                pct_change = (price_change / prev_close) * 100
                delta_class = "yh-delta-pos" if price_change >= 0 else "yh-delta-neg"
                delta_sign = "+" if price_change >= 0 else ""
                
                st.markdown(f"""
                    <div class="yh-header">
                        <p style="color: #8b949e; font-size: 0.9rem; margin-bottom: 0.2rem;">{info.get('exchange', 'Exchange')}</p>
                        <h1 class="yh-company-name">{company_name} ({ticker_symbol})</h1>
                        <div class="yh-price-container">
                            <span class="yh-current-price">{curr_price:,.2f}</span>
                            <span class="{delta_class}">{delta_sign}{price_change:,.2f} ({delta_sign}{pct_change:.2f}%)</span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            
            # Layout with Tabs
            tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Statistics", "News", "Financials"])

            with tab1:
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric(label="Previous Close", value=f"${prev_close:,.2f}" if prev_close else "N/A")
                with col2:
                    st.metric(label="Day High", value=f"${info.get('dayHigh', 0):,.2f}")
                with col3:
                    st.metric(label="Day Low", value=f"${info.get('dayLow', 0):,.2f}")
                with col4:
                    st.metric(label="Volume", value=f"{info.get('regularMarketVolume', 0):,}")

                # Main Chart
                period = st.select_slider("Select Timeframe", options=['1d', '5d', '1mo', '3mo', '6mo', '1y', '5y', 'max'], value='1y', key="overview_period")
                history = ticker.history(period=period)
                
                if not history.empty:
                    chart_color = "#00ff73" if (history['Close'].iloc[-1] >= history['Close'].iloc[0]) else "#ff333a"
                    
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(
                        x=history.index, 
                        y=history['Close'], 
                        line=dict(color=chart_color, width=2),
                        name="Close Price"
                    ))

                    fig.update_layout(
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='#8b949e'),
                        xaxis=dict(showgrid=False, zeroline=False),
                        yaxis=dict(showgrid=True, gridcolor='#30363d', side='right'),
                        margin=dict(l=0, r=0, t=10, b=0),
                        height=400,
                        hovermode="x unified"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                st.markdown("---")
                st.subheader("Description")
                st.write(info.get('longBusinessSummary', 'No summary available.'))

            with tab2:
                st.subheader("Key Statistics")
                stats_col1, stats_col2 = st.columns(2)
                
                with stats_col1:
                    data1 = {
                        "Metric": ["PE Ratio (Trailing)", "Forward PE", "PEG Ratio", "Price to Sales", "Beta"],
                        "Value": [str(info.get('trailingPE', 'N/A')), str(info.get('forwardPE', 'N/A')), str(info.get('pegRatio', 'N/A')), str(info.get('priceToSalesTrailing12Months', 'N/A')), str(info.get('beta', 'N/A'))]
                    }
                    st.table(pd.DataFrame(data1))
                
                with stats_col2:
                    data2 = {
                        "Metric": ["Dividend Yield", "Profit Margin", "Return on Equity", "Total Cash", "Total Debt"],
                        "Value": [f"{info.get('dividendYield', 0)*100:.2f}%" if info.get('dividendYield') else "N/A", 
                                  f"{info.get('profitMargins', 0)*100:.2f}%" if info.get('profitMargins') else "N/A",
                                  f"{info.get('returnOnEquity', 0)*100:.2f}%" if info.get('returnOnEquity') else "N/A",
                                  f"${info.get('totalCash', 0):,}" if isinstance(info.get('totalCash'), (int, float)) else "N/A",
                                  f"${info.get('totalDebt', 0):,}" if isinstance(info.get('totalDebt'), (int, float)) else "N/A"]
                    }
                    st.table(pd.DataFrame(data2))

            with tab3:
                st.subheader(f"Latest News for {ticker_symbol}")
                news = ticker.news
                if news:
                    for item in news[:8]:
                        with st.container():
                            st.markdown(f"#### [{item['title']}]({item['link']})")
                            st.write(f"*Source: {item['publisher']}*")
                            st.markdown("---")
                else:
                    st.info("No recent news found for this ticker.")

            with tab4:
                st.subheader("Financial Statements")
                f_tab1, f_tab2, f_tab3 = st.tabs(["Income Statement", "Balance Sheet", "Cash Flow"])
                
                with f_tab1:
                    try:
                        st.dataframe(ticker.income_stmt, use_container_width=True)
                    except: st.warning("Income Statement data unavailable.")
                
                with f_tab2:
                    try:
                        st.dataframe(ticker.balance_sheet, use_container_width=True)
                    except: st.warning("Balance Sheet data unavailable.")

                with f_tab3:
                    try:
                        st.dataframe(ticker.cashflow, use_container_width=True)
                    except: st.warning("Cash Flow data unavailable.")

    except Exception as e:
        st.error(f"Something went wrong while fetching data: {e}")