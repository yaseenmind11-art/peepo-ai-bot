# --- 2. THEME STYLING ---
st.markdown("""
<style>
/* 1. DEFAULT/LIGHT THEME */
/* This handles the blue/purple fade when the theme is set to Light */
[data-theme="light"] .stApp, .stApp {
    background: linear-gradient(135deg, #d1e9ff 0%, #e1d5f5 50%, #ffffff 100%) !important;
}

[data-theme="light"] .p-sticker, 
[data-theme="light"] [data-testid="stchatAvatarAssistant"] img,
[data-theme="light"] [data-testid="stImage"] img {
    filter: none !important; /* Keep logo black in light mode */
}

/* 2. DARK THEME */
/* This triggers when you manually select 'Dark' or your system is dark */
[data-theme="dark"] .stApp, 
[data-theme="dark"] [data-testid="stHeader"],
@media (prefers-color-scheme: dark) {
    [data-theme="dark"] .stApp,
    [data-theme="dark"] [data-testid="stHeader"] {
        background-color: #000000 !important;
        background-image: none !important;
    }
    
    /* Invert logo to white only in dark mode */
    [data-theme="dark"] .p-sticker, 
    [data-theme="dark"] [data-testid="stchatAvatarAssistant"] img,
    [data-theme="dark"] [data-testid="stImage"] img {
        filter: invert(1) brightness(2) !important;
    }

    [data-theme="dark"] [data-testid="stSidebar"] {
        background-color: #0a0a0a !important;
    }

    [data-theme="dark"] h1, [data-theme="dark"] h2, [data-theme="dark"] p {
        color: #ffffff !important;
    }
}

/* Layout Fixes */
.centered-logo {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-bottom: -40px;
}
</style>
""", unsafe_allow_html=True)
