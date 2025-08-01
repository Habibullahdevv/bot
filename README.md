# OTC Binary Options Prediction Bot

## Overview
This is a secure, single-user, web-based prediction bot for OTC and regular binary options markets, supporting popular brokers like Quotex, Pocket Option, Expert Option, and IQ Option. The bot generates "buy", "sell", or "hold" signals using an ensemble of technical indicators.

## Features
- Single-user login system for security
- Select broker, OTC or regular market, asset, and timeframe
- Data fetched via Selenium scraping and public APIs fallback
- Ensemble of EMA crossover, RSI, Stochastic Oscillator, and Candlestick pattern strategies
- Display of confidence scores and individual strategy signals
- Responsive UI built with Streamlit

## Installation
1. Clone repo and navigate into folder
2. Create `.env` file from `.env.example` and set your `STREAMLIT_USER` and `STREAMLIT_PASS`
3. Install dependencies
