import pandas as pd
import numpy as np
import ta
from ta.momentum import StochasticOscillator
from ta.trend import EMAIndicator
from ta.momentum import RSIIndicator

def ema_crossover(df, short_window=3, long_window=8):
    ema_short = EMAIndicator(close=df['close'], window=short_window).ema_indicator()
    ema_long = EMAIndicator(close=df['close'], window=long_window).ema_indicator()
    df['ema_short'] = ema_short
    df['ema_long'] = ema_long
    if ema_short.iloc[-1] > ema_long.iloc[-1] and ema_short.iloc[-2] <= ema_long.iloc[-2]:
        return "buy"
    elif ema_short.iloc[-1] < ema_long.iloc[-1] and ema_short.iloc[-2] >= ema_long.iloc[-2]:
        return "sell"
    else:
        return "hold"

def rsi_strategy(df, window=14, overbought=70, oversold=30):
    rsi = RSIIndicator(close=df['close'], window=window).rsi()
    if rsi.iloc[-1] < oversold:
        return "buy"
    elif rsi.iloc[-1] > overbought:
        return "sell"
    else:
        return "hold"

def stochastic_strategy(df, window=14, smooth_window=3, overbought=80, oversold=20):
    stoch = StochasticOscillator(high=df['high'], low=df['low'], close=df['close'], window=window, smooth_window=smooth_window)
    k = stoch.stoch()
    if k.iloc[-1] < oversold:
        return "buy"
    elif k.iloc[-1] > overbought:
        return "sell"
    else:
        return "hold"

def candlestick_pattern(df):
    # Very basic pattern detection for Doji, Hammer, Engulfing (last candle)
    candle = df.iloc[-1]
    body = abs(candle['close'] - candle['open'])
    candle_range = candle['high'] - candle['low']
    upper_shadow = candle['high'] - max(candle['close'], candle['open'])
    lower_shadow = min(candle['close'], candle['open']) - candle['low']

    # Doji detection: body very small
    if body <= 0.1 * candle_range:
        return "hold"  # Neutral for now
    # Hammer detection (small body lower end, long lower shadow)
    if lower_shadow > 2 * body and upper_shadow < 0.1 * body:
        return "buy"
    # Shooting star (inverse hammer)
    if upper_shadow > 2 * body and lower_shadow < 0.1 * body:
        return "sell"
    # Otherwise hold
    return "hold"

def ensemble_signals(df, market_type="regular"):
    """
    Aggregate signals from all strategies with weighting
    """
    # Adjust parameters for OTC market
    if market_type == "otc":
        rsi_signal = rsi_strategy(df, window=7, overbought=65, oversold=35)
        ema_signal = ema_crossover(df, short_window=2, long_window=5)
    else:
        rsi_signal = rsi_strategy(df)
        ema_signal = ema_crossover(df)

    stoch_signal = stochastic_strategy(df)
    candle_signal = candlestick_pattern(df)

    signals = [rsi_signal, ema_signal, stoch_signal, candle_signal]

    buys = signals.count("buy")
    sells = signals.count("sell")

    # Voting system
    if buys > sells and buys >= 2:
        final_signal = "buy"
        confidence = buys / len(signals)
    elif sells > buys and sells >= 2:
        final_signal = "sell"
        confidence = sells / len(signals)
    else:
        final_signal = "hold"
        confidence = 0.0

    return final_signal, confidence, signals
