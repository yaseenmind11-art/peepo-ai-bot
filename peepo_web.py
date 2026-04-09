import streamlit as st
import os

# --- 1. GOOGLE FILE VERIFICATION LOGIC ---
# This part handles the HTML file you just uploaded!
import base64

# Replace 'google470ff30df2261297.html' with your EXACT filename from GitHub
VERIFICATION_FILE = "google470ff30df2261297.html"

# If Google looks for the file, we serve it directly
query_params = st.query_params
if VERIFICATION_FILE in query_params or "verify" in query_params:
    st.write("google-site-verification: google470ff30df2261297.html")
    st.stop()

# --- 2. PAGE CONFIG & THEME ---
st.set_page_config(page_title="Peepo 3 AI", page_icon="image_13ffcc.png")

st.markdown(r"""
<style>
/* LIGHT THEME */
[data-theme="light"] .stApp, .stApp {
    background: linear-gradient(135deg, #d1e9ff 0%, #e1d5f5 50%, #ffffff 100%) !important;
}
/* DARK THEME */
[data-theme="dark"] .stApp { background-color: #000000 !important; }
[data-theme="dark"] .p-sticker { filter: invert(1) brightness(2) !important; }
.centered-logo { display: flex; justify-content: center; margin-bottom: -40px; }
</style>
""", unsafe_allow_html=True)

# --- 3. MAIN APP INTERFACE ---
LOGO_PATH = "image_13ffcc.png"
st.markdown('<div class="centered-logo">', unsafe_allow_html=True)
if os.path.exists(LOGO_PATH):
    st.image(LOGO_PATH, width=130)
st.markdown('</div>', unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center;'>Welcome to Peepo 3</h1>", unsafe_allow_html=True)

# (Rest of your chat logic here...)
