import streamlit as st
from google import genai
import os

# --- 1. PAGE CONFIG ---
st.set_page_config(page_title="Peepo 3 AI", page_icon="image_13ffcc.png")

# --- 2. GOOGLE VERIFICATION (ONLY) ---
# We removed the styling for a moment so Google can see this clearly!
st.write(f'<meta name="google-site-verification" content="W9JcAjDYAJtTHQz2toGnqDUsgQo34tcEmQSf-NItZug" />', unsafe_allow_html=True)

# --- 3. BASIC UI ---
st.title("Welcome to Peepo 3")
st.write("Verification in progress...")

# --- 4. API & LOGIC ---
try:
    API_KEY = st.secrets["GEMINI_API_KEY"].strip().replace('"', '')
    client = genai.Client(api_key=API_KEY)
except:
    pass
