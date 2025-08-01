import os
from dotenv import load_dotenv

load_dotenv()

STREAMLIT_USER = os.getenv("STREAMLIT_USER", "admin")
STREAMLIT_PASS = os.getenv("STREAMLIT_PASS", "password")

# Timeout for session (in seconds)
SESSION_TIMEOUT = 7200  # 2 hours

# Supported brokers and markets
BROKERS = {
    "Quotex": {
        "OTC": True,
        "assets": ["USD/BRL", "EUR/USD", "Gold", "Oil", "BTC/USD"],
    },
    "Pocket Option": {
        "OTC": True,
        "assets": ["USD/BRL", "EUR/USD", "Gold", "Silver"],
    },
    "Expert Option": {
        "OTC": True,
        "assets": ["EUR/USD", "GBP/USD", "NASDAQ", "Crypto"],
    },
    "IQ Option": {
        "OTC": True,
        "assets": ["EUR/USD", "USD/JPY", "Gold", "BTC/USD"],
    },
}

# Timeframes in seconds for easy processing
TIMEFRAMES = [5, 15, 30, 45, 60, 65, 75, 90, 105, 120]
TIMEFRAME_LABELS = [
    "5s", "15s", "30s", "45s", "1min", "1:05min", "1:15min", "1:30min", "1:45min", "2min"
]

# Selenium options
SELENIUM_HEADLESS = True

# Logging and debug
LOGGING_LEVEL = "INFO"
