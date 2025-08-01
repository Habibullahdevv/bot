#!/bin/bash

echo "Setting up Python environment and installing dependencies..."

python3 -m venv venv
source venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

echo "Setup complete. Run 'source venv/bin/activate' and then 'streamlit run app.py' to start the bot."
