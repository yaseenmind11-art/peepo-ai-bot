import streamlit as st
from google import genai
from google.genai import types
import os

# 1. IMMEDIATE SESSION INITIALIZATION (Fixes the new error)
# This must happen before ANY other logic to prevent the "no attribute all_chats" crash.
if "all_chats" not in st.session_state:
    st.session_state.all_chats = {} 
if "current_chat" not in st.session_state:
    st.session_state.current_chat = None 

# 2. PAGE SETUP
st.set_page_config(page_title="peepo 3 ai", page_icon="image_13ffcc.png")

# [Insert your existing CSS/Theming here]

# 3. API SETUP
try:
    API_KEY = st.secrets["GEMINI_API_KEY"].strip().replace('"', '')
    client = genai.Client(api_key=API_KEY)
except Exception:
    st.error("⚠️ API Key missing in Secrets!")

# 4. SIDEBAR & HISTORY
with st.sidebar:
    st.title("📂 Peepo History")
    if st.button("➕ New Chat", use_container_width=True):
        st.session_state.current_chat = None 
        st.rerun()
    st.divider()
    # Safely iterate through history
    for chat_title in list(st.session_state.all_chats.keys()):
        if st.button(chat_title, key=f"btn_{chat_title}", use_container_width=True):
            st.session_state.current_chat = chat_title
            st.rerun()

# 5. CHAT LOGIC (THE STABILITY PATCH)
if prompt := st.chat_input("Message peepo 3 ai..."):
    # Check session state again before appending
    if st.session_state.current_chat is None:
        new_title = prompt[:25]
        st.session_state.current_chat = new_title
        st.session_state.all_chats[new_title] = []
    
    st.session_state.all_chats[st.session_state.current_chat].append({"role": "user", "content": prompt})
    
    try:
        # Use the "Flash-Lite" model - it has the highest free quota in 2026
        response = client.models.generate_content(
            model="gemini-2.0-flash-lite", 
            config=types.GenerateContentConfig(
                system_instruction="You are Peepo-Sec, a White Hat Hacker."
            ),
            contents=prompt
        )
        st.session_state.all_chats[st.session_state.current_chat].append({"role": "assistant", "content": response.text})
        st.rerun()

    except Exception as e:
        if "429" in str(e):
            st.error("🚦 Google's free tier is maxed out. Even if you wait, the server is busy. Try again in 5 minutes.")
        else:
            st.error(f"Error: {e}")
