import streamlit as st

# --- Custom Theme Styles ---
st.markdown("""
    <style>
    /* General page styling */
    body, .stApp {
        background-color: var(--background-color);
        color: var(--text-color);
        transition: all 0.3s ease-in-out;
    }

    /* Define light and dark theme colors */
    @media (prefers-color-scheme: light) {
        :root {
            --background-color: #f9f9fb;
            --text-color: #111;
            --card-bg: #ffffff;
            --border-color: #ccc;
            --highlight: #0077b6;
            --button-bg: #0077b6;
            --button-text: #ffffff;
        }
    }

    @media (prefers-color-scheme: dark) {
        :root {
            --background-color: #0d1117;
            --text-color: #e0e0e0;
            --card-bg: #161b22;
            --border-color: #30363d;
            --highlight: #58a6ff;
            --button-bg: #238636;
            --button-text: #ffffff;
        }
    }

    /* Title */
    h1 {
        text-align: center;
        color: var(--highlight);
        font-weight: 700;
        font-size: 2.5rem;
    }

    /* Subheader text */
    .subtitle {
        text-align: center;
        color: var(--text-color);
        font-size: 1.1rem;
        margin-bottom: 1rem;
    }

    /* Instruction Box */
    .instruction-box {
        background-color: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }

    .instruction-box b {
        color: var(--highlight);
    }

    /* Input Fields */
    .stSelectbox, .stTextInput {
        background-color: var(--card-bg) !important;
        color: var(--text-color) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 10px !important;
    }

    /* Buttons */
    .stButton>button {
        background-color: var(--button-bg) !important;
        color: var(--button-text) !important;
        border-radius: 10px !important;
        border: none !important;
        padding: 0.6rem 1.2rem !important;
        font-weight: 600 !important;
    }

    .stButton>button:hover {
        opacity: 0.9 !important;
        transform: scale(1.02);
        transition: all 0.2s ease-in-out;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: var(--text-color);
        font-size: 0.9rem;
        margin-top: 3rem;
        opacity: 0.7;
    }
    </style>
""", unsafe_allow_html=True)

# --- Page Content ---
st.markdown("<h1>Village Khasra Chatbot 💬</h1>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Search village land details with ease — clean, readable, professional.</div>", unsafe_allow_html=True)

st.markdown("""
<div class='instruction-box'>
<b>How to Use:</b><br>
Choose your Village from the dropdown → Enter Khasra number → Click on Search 🔍
</div>
""", unsafe_allow_html=True)

village = st.selectbox("🏡 Select a Village", ["Ababkaspur", "Asalatpur", "Aminagar", "Jalalpur", "Rehra", "Tanda", "Bilari"])
khasra = st.text_input("📘 Enter Khasra Number")
if st.button("Search 🔍"):
    st.success(f"Searching for Khasra {khasra} in {village}...")

st.markdown("<div class='footer'>Made with 💻 by Moradabad Development Authority</div>", unsafe_allow_html=True)


















