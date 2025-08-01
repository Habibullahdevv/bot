import streamlit as st
import hashlib
import time
from config import STREAMLIT_USER, STREAMLIT_PASS, SESSION_TIMEOUT

def hash_password(password: str) -> str:
    return hashlib.pbkdf2_hmac('sha256', password.encode(), b'salt', 100000).hex()

def check_credentials(username: str, password: str) -> bool:
    return username == STREAMLIT_USER and hash_password(password) == hash_password(STREAMLIT_PASS)

def login():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if not st.session_state.authenticated:
        st.title("🔐 Login to Trading Bot")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if check_credentials(username, password):
                st.session_state.authenticated = True
                st.session_state.last_active = time.time()
                st.success("✅ Login successful!")
                st.rerun()  # THIS IS THE FIXED LINE
            else:
                st.error("❌ Invalid username or password")
        return False
    else:
        if time.time() - st.session_state.get("last_active", 0) > SESSION_TIMEOUT:
            st.session_state.authenticated = False
            st.warning("⏰ Session expired. Please login again.")
            st.rerun()  # THIS IS THE FIXED LINE
            return False
        else:
            st.session_state.last_active = time.time()
            if st.sidebar.button("🚪 Logout"):
                st.session_state.authenticated = False
                st.rerun()  # THIS IS THE FIXED LINE
            return True
