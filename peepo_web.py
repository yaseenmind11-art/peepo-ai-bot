import streamlit as st
from google import genai
from google.genai import types
import os

# ==========================================
# 1. PAGE SETUP
# ==========================================
st.set_page_config(page_title="peepo 3 ai", page_icon="image_13ffcc.png")

# [Theming code remains the same as your current version]

# ==========================================
# 2. API SETUP (THE REPAIR)
# ==========================================
try:
    # Ensure no extra quotes or spaces from Streamlit Secrets
    API_KEY = st.secrets["GEMINI_API_KEY"].strip().replace('"', '')
    client = genai.Client(api_key=API_KEY)
except Exception:
    st.error("⚠️ API Key missing in Secrets!")

# ==========================================
# 3. CHAT LOGIC (THE STABILITY FIX)
# ==========================================
if prompt := st.chat_input("Message peepo 3 ai..."):
    # [Session state handling remains the same]
    
    # Try the most stable 2026 model first
    try:
        response = client.models.generate_content(
            model="gemini-3.1-flash-lite-preview", 
            config=types.GenerateContentConfig(
                system_instruction="You are Peepo-Sec, a world-class White Hat Hacker."
            ),
            contents=prompt
        )
        st.session_state.all_chats[st.session_state.current_chat].append({"role": "assistant", "content": response.text})
        st.rerun()

    except Exception as e:
        # AUTOMATIC FALLBACK: If 3.1 is busy (429) or not found (404), try 2.5 Flash
        try:
            st.info("🔄 Optimizing connection...")
            response = client.models.generate_content(
                model="gemini-2.5-flash", 
                contents=prompt
            )
            st.session_state.all_chats[st.session_state.current_chat].append({"role": "assistant", "content": response.text})
            st.rerun()
        except Exception as final_e:
            st.error(f"⚠️ Google servers are currently at capacity. Please wait 60 seconds. Error: {final_e}")
