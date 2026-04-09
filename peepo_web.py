import streamlit as st
import streamlit.components.v1 as components
from google import genai
import os

# --- 1. PAGE CONFIG ---
st.set_page_config(page_title="Peepo 3 AI", page_icon="image_13ffcc.png")

# --- 2. INVISIBLE GOOGLE VERIFICATION ---
# This tag stays hidden from users but Google will find it!
components.html('<meta name="google-site-verification" content="W9JcAjDYAJtTHQz2toGnqDUsgQo34tcEmQSf-NItZug" />', height=0)

# --- 3. THEME STYLING ---
st.markdown(r"""
<style>
/* LIGHT THEME */
[data-theme="light"] .stApp, .stApp {
    background: linear-gradient(135deg, #d1e9ff 0%, #e1d5f5 50%, #ffffff 100%) !important;
}
/* DARK THEME */
[data-theme="dark"] .stApp, [data-theme="dark"] [data-testid="stHeader"] {
    background-color: #000000 !important;
}
[data-theme="dark"] .p-sticker, 
[data-theme="dark"] [data-testid="stchatAvatarAssistant"] img {
    filter: invert(1) brightness(2) !important;
}
.centered-logo { display: flex; justify-content: center; margin-bottom: -40px; }
</style>
""", unsafe_allow_html=True)

# --- 4. MAIN INTERFACE ---
LOGO_PATH = "image_13ffcc.png"
st.markdown('<div class="centered-logo">', unsafe_allow_html=True)
if os.path.exists(LOGO_PATH):
    st.image(LOGO_PATH, width=130)
st.markdown('</div>', unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center;'>Welcome to Peepo 3</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; opacity: 0.8;'>Ready for some Arduino coding or science help?</p>", unsafe_allow_html=True)

# Add your chat logic here...
