import streamlit as st
from google import genai
from google.genai import types
import os

# 1. CRITICAL: Initialize Session BEFORE everything else
# This prevents the white screen crash on refresh
if "all_chats" not in st.session_state:
    st.session_state.all_chats = {} 
if "current_chat" not in st.session_state:
    st.session_state.current_chat = None 

# 2. PAGE SETUP
st.set_page_config(page_title="peepo 3 ai", page_icon="image_13ffcc.png")

# [Your existing CSS/Theming code goes here]

# 3. API CONNECTION (STABLE 2026 ENDPOINT)
try:
    API_KEY = st.secrets["GEMINI_API_KEY"].strip().replace('"', '')
    client = genai.Client(api_key=API_KEY)
except Exception:
    st.error("⚠️ API Key missing!")

# 4. CHAT LOGIC (USING ACTIVE 2026 MODELS)
if prompt := st.chat_input("Message peepo 3 ai..."):
    if st.session_state.current_chat is None:
        new_title = prompt[:25]
        st.session_state.current_chat = new_title
        st.session_state.all_chats[new_title] = []
    
    st.session_state.all_chats[st.session_state.current_chat].append({"role": "user", "content": prompt})
    
    try:
        # THE FIX: gemini-3.1-flash-lite-preview is the most stable free model right now
        response = client.models.generate_content(
            model="gemini-3.1-flash-lite-preview", 
            config=types.GenerateContentConfig(
                system_instruction="You are Peepo-Sec, a White Hat Hacker."
            ),
            contents=prompt
        )
        st.session_state.all_chats[st.session_state.current_chat].append({"role": "assistant", "content": response.text})
        st.rerun()

    except Exception as e:
        # Fallback to 2.5 Flash if 3.1 is at its limit
        try:
            response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
            st.session_state.all_chats[st.session_state.current_chat].append({"role": "assistant", "content": response.text})
            st.rerun()
        except:
            st.error("🚦 All Google free-tier servers are full. Please wait 60 seconds!")
