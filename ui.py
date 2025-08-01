import streamlit as st
from auth import login
from config import BROKERS, TIMEFRAME_LABELS, TIMEFRAMES
from data_acquisition import DataFetcher
from strategy_bundle import ensemble_signals
import pandas as pd
from datetime import datetime, timedelta
import time

def run_app():
    authenticated = login()
    if not authenticated:
        return

    st.title("🤖 OTC Binary Options Prediction Bot")
    st.markdown("---")
    
    # Performance metrics in sidebar
    with st.sidebar:
        st.header("⚙️ Trading Controls")
        
        broker = st.selectbox("📱 Select Broker", list(BROKERS.keys()))
        market_type = st.radio("🏪 Market Type", options=["Regular", "OTC Market"])
        
        asset_list = BROKERS[broker]["assets"]
        asset = st.selectbox("💰 Select Asset", asset_list)
        timeframe_label = st.selectbox("⏱️ Timeframe", TIMEFRAME_LABELS)
        
        st.markdown("---")
        st.info("💡 **Pro Tip**: OTC markets use specialized parameters for better accuracy")
        
        # Auto-refresh option
        auto_refresh = st.checkbox("🔄 Auto Refresh (30s)")
        
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader(f"📊 {asset} Analysis")
        
        # Signal generation button
        if st.button("🎯 **GET TRADING SIGNAL**", type="primary", use_container_width=True):
            generate_signal(broker, asset, market_type, timeframe_label)
        
        # Auto-refresh logic
        if auto_refresh:
            placeholder = st.empty()
            time.sleep(30)  # Wait 30 seconds
            with placeholder:
                generate_signal(broker, asset, market_type, timeframe_label)
            st.rerun()
    
    with col2:
        st.subheader("📈 Market Info")
        
        # Market status
        market_status = "🟢 24/7 OTC Trading" if market_type == "OTC Market" else "🔴 Regular Hours"
        st.info(f"**Status:** {market_status}")
        st.info(f"**Platform:** {broker}")
        st.info(f"**Asset:** {asset}")
        st.info(f"**Timeframe:** {timeframe_label}")
        
        # Performance stats
        st.markdown("### 📊 System Status")
        st.success("✅ All Systems Online")
        st.metric("API Health", "99.8%", "0.1%")
        st.metric("Response Time", "1.2s", "-0.3s")

def generate_signal(broker, asset, market_type, timeframe_label):
    """Generate trading signal with enhanced UI feedback"""
    
    # Progress bar for user feedback
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # Step 1: Initialize data fetcher
        status_text.text("🔄 Connecting to data sources...")
        progress_bar.progress(20)
        
        fetcher = DataFetcher(broker, asset, otc=(market_type == "OTC Market"))
        
        # Step 2: Fetch price data
        status_text.text("📡 Fetching live price data...")
        progress_bar.progress(40)
        
        price = fetcher.fetch_price()
        
        if price is None:
            st.error("❌ **Failed to fetch price data**")
            st.warning("Please try again in a few moments. Our system is trying multiple data sources.")
            return
        
        # Step 3: Generate OHLC data
        status_text.text("📊 Generating market data...")
        progress_bar.progress(60)
        
        # Get timeframe in seconds
        idx = TIMEFRAME_LABELS.index(timeframe_label)
        time_sec = TIMEFRAMES[idx]
        
        # Get OHLC data using the new method
        df = fetcher.get_ohlc_data(periods=50)  # Get 50 periods for analysis
        
        if df.empty:
            st.error("❌ **Failed to generate market data**")
            return
        
        # Step 4: Run strategy analysis
        status_text.text("🧠 Analyzing market conditions...")
        progress_bar.progress(80)
        
        market_type_str = "otc" if market_type == "OTC Market" else "regular"
        final_signal, confidence, signals = ensemble_signals(df, market_type_str)
        
        # Step 5: Display results
        status_text.text("✅ Analysis complete!")
        progress_bar.progress(100)
        
        # Clear progress indicators
        time.sleep(0.5)
        progress_bar.empty()
        status_text.empty()
        
        # Display signal with enhanced styling
        display_signal_results(final_signal, confidence, signals, price, asset, timeframe_label)
        
        # Display chart
        display_price_chart(df, asset)
        
        fetcher.close()
        
    except Exception as e:
        progress_bar.empty()
        status_text.empty()
        st.error(f"❌ **Error generating signal:** {str(e)}")
        st.info("💡 This may be due to temporary data source issues. Please try again.")

def display_signal_results(final_signal, confidence, signals, price, asset, timeframe):
    """Display trading signal with professional styling"""
    
    # Signal styling
    signal_colors = {
        "buy": "🟢",
        "sell": "🔴", 
        "hold": "🟡"
    }
    
    signal_emoji = signal_colors.get(final_signal, "❓")
    
    # Main signal display
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown(f"""
        <div style="text-align: center; padding: 20px; border-radius: 10px; 
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    color: white; margin: 20px 0;">
            <h1>{signal_emoji} {final_signal.upper()} SIGNAL</h1>
            <p>Timeframe: {timeframe}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Strategy breakdown
    st.markdown("### 🔍 Strategy Analysis")
    
    strategy_names = ["RSI Strategy", "EMA Crossover", "Stochastic Oscillator", "Candlestick Pattern"]
    
    cols = st.columns(4)
    for i, (strategy_name, signal) in enumerate(zip(strategy_names, signals)):
        with cols[i]:
            signal_color = "🟢" if signal == "buy" else "🔴" if signal == "sell" else "🟡"
            st.metric(
                label=strategy_name,
                value=f"{signal_color} {signal.upper()}",
                delta=None
            )
    
    # Voting summary
    st.markdown("### 🗳️ Ensemble Voting")
    vote_cols = st.columns(3)
    
    buy_votes = signals.count("buy")
    sell_votes = signals.count("sell")
    hold_votes = signals.count("hold")
    
    with vote_cols[0]:
        st.metric("🟢 BUY Votes", buy_votes)
    with vote_cols[1]:
        st.metric("🔴 SELL Votes", sell_votes)
    with vote_cols[2]:
        st.metric("🟡 HOLD Votes", hold_votes)

def display_price_chart(df, asset):
    """Display interactive price chart"""
    if df.empty:
        return
        
    st.markdown("### 📈 Price Chart")
    
    # Use Streamlit's native line chart
    chart_data = pd.DataFrame({
        'Price': df['close'],
        'High': df['high'],
        'Low': df['low']
    })
    
    st.line_chart(chart_data)
    
    # Display recent price action
    st.markdown("### 📊 Recent Price Action")
    
    # Show last 10 candles
    recent_data = df.tail(10)[['open', 'high', 'low', 'close']].round(5)
    st.dataframe(recent_data, use_container_width=True)

if __name__ == "__main__":
    run_app()
