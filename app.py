import streamlit as st
import pandas as pd

st.set_page_config(page_title="Village Khasra Chatbot", page_icon="💬", layout="centered")

# --- STYLING ---
st.markdown("""
    <style>
    :root {
        --main-color: #00E0FF;
        --bg-gradient-dark: radial-gradient(circle at top left, #0b0c10, #1f2833);
        --bg-gradient-light: linear-gradient(135deg, #f5f7fa, #c3cfe2);
        --card-bg-dark: rgba(255,255,255,0.05);
        --card-bg-light: rgba(0,0,0,0.05);
        --text-light: #f9f9f9;
        --text-dark: #1b1b1b;
    }

    [data-testid="stAppViewContainer"] {
        background: var(--bg-gradient-dark);
        color: var(--text-light);
    }
    [data-theme="light"] [data-testid="stAppViewContainer"] {
        background: var(--bg-gradient-light);
        color: var(--text-dark);
    }

    h1 {
        text-align: center;
        font-size: 2.6rem;
        font-weight: 800;
        text-shadow: 0 0 15px rgba(0,224,255,0.7);
        color: var(--main-color);
    }

    p, label, div, span {
        font-family: "Inter", sans-serif;
    }

    /* Instruction + Disclaimer Cards */
    .info-card {
        background: var(--card-bg-dark);
        padding: 1.5rem 1.8rem;
        border-radius: 16px;
        margin-bottom: 1.8rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        transition: all 0.3s ease-in-out;
    }
    [data-theme="light"] .info-card {
        background: var(--card-bg-light);
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }

    .info-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 25px rgba(0,224,255,0.3);
    }

    .info-title {
        font-weight: 700;
        font-size: 1.1rem;
        color: var(--main-color);
        margin-bottom: 0.5rem;
    }

    /* Inputs */
    .stSelectbox div div, .stTextInput input {
        border: 1px solid rgba(0,224,255,0.4) !important;
        border-radius: 10px !important;
        background-color: rgba(0,0,0,0.2) !important;
        color: inherit !important;
        transition: 0.2s;
    }

    [data-theme="light"] .stSelectbox div div, [data-theme="light"] .stTextInput input {
        background-color: rgba(255,255,255,0.8) !important;
        color: var(--text-dark) !important;
    }

    .stSelectbox div div:focus-within, .stTextInput input:focus {
        box-shadow: 0 0 12px rgba(0,224,255,0.7);
        border-color: var(--main-color);
    }

    /* Button */
    button[kind="primary"] {
        background: linear-gradient(90deg, #00C6FF, #0072FF);
        color: white !important;
        border-radius: 10px !important;
        border: none !important;
        font-weight: bold;
        padding: 0.4rem 1.4rem;
        box-shadow: 0 0 12px rgba(0,224,255,0.4);
        transition: all 0.25s ease-in-out;
    }

    button[kind="primary"]:hover {
        transform: scale(1.05);
        box-shadow: 0 0 18px rgba(0,224,255,0.6);
    }

    /* Data Table */
    [data-testid="stDataFrame"] {
        border-radius: 10px !important;
        overflow: hidden !important;
    }

    /* Disclaimer */
    .disclaimer {
        margin-top: 2.5rem;
        text-align: center;
        font-size: 0.9rem;
        line-height: 1.6;
        opacity: 0.8;
        background: var(--card-bg-dark);
        padding: 1rem 1.5rem;
        border-radius: 12px;
        box-shadow: 0 0 15px rgba(0,0,0,0.3);
    }
    [data-theme="light"] .disclaimer {
        background: var(--card-bg-light);
    }
    </style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown("<h1>Village Khasra Chatbot</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Search village land details with ease — clean, readable, professional.</p>", unsafe_allow_html=True)

# --- INSTRUCTIONS CARD ---
st.markdown("""
<div class='info-card'>
    <div class='info-title'>How to Use</div>
    <p>1. Choose a Village from the dropdown.</p>
    <p>2. Enter the Khasra number in the input box.</p>
    <p>3. Click on the <b>Search</b> button to view land details.</p>
</div>
""", unsafe_allow_html=True)

# --- INPUT SECTION ---
village = st.selectbox("Select a Village", ["Ababbaspur", "Mau", "Bilari"])
khasra = st.text_input("Enter Khasra Number")

# --- SEARCH BUTTON + TABLE ---
if st.button("Search"):
    if not khasra.strip():
        st.warning("Please enter a Khasra number to search.")
    else:
        st.success("Khasra Details Found")
        df = pd.DataFrame({
            "Village": [village]*3,
            "Khasra": [khasra]*3,
            "Land use": ["Agriculture", "Residential", "Green Belt"],
            "Latitude": [28.84, 28.85, 28.86],
            "Longitude": [78.76, 78.77, 78.78]
        })
        st.dataframe(df)

# --- DISCLAIMER (Bilingual) ---
st.markdown("""
<div class='disclaimer'>
    <b>Disclaimer:</b><br>
    The data displayed here is for informational purposes only. Users are advised to verify land and khasra details from the official records of the <b>Moradabad Development Authority</b> before taking any decisions.<br><br>
    यहाँ प्रदर्शित आंकड़े केवल जानकारी हेतु हैं। उपयोगकर्ताओं को सलाह दी जाती है कि वे किसी भी निर्णय से पहले <b>मुरादाबाद विकास प्राधिकरण</b> के आधिकारिक अभिलेखों से भूखंड एवं खसरा विवरण की पुष्टि करें।
</div>
""", unsafe_allow_html=True)










