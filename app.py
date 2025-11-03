import streamlit as st
import pandas as pd

# --- PAGE CONFIG ---
st.set_page_config(page_title="Village Khasra Chatbot", page_icon="💬", layout="centered")

# --- UNIVERSAL STYLING ---
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, var(--background-color), var(--secondary-background-color));
        color: var(--text-color);
    }
    h1, h2, h3, h4, h5, h6, p, label, span, div {
        color: var(--text-color);
    }
    .stTextInput > div > div > input,
    .stSelectbox > div > div > div {
        color: var(--text-color) !important;
        background-color: var(--background-color) !important;
        border: 1px solid rgba(128,128,128,0.4) !important;
        border-radius: 8px !important;
    }
    ::placeholder {
        color: rgba(128,128,128,0.8);
    }
    button[kind="primary"] {
        background: linear-gradient(90deg, #00C6FF, #0072FF);
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: bold;
    }
    .instruction-box {
        background-color: rgba(128,128,128,0.15);
        padding: 1.2rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
    }
    .disclaimer {
        font-size: 0.9rem;
        color: var(--text-color);
        opacity: 0.85;
        text-align: center;
        margin-top: 2.5rem;
        padding-top: 0.8rem;
        border-top: 1px solid rgba(128,128,128,0.3);
        line-height: 1.6;
    }
    </style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown("<h1 style='text-align:center;'>Village Khasra Chatbot 💬</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Search village land details with ease — clean, readable, professional.</p>", unsafe_allow_html=True)

# --- HOW TO USE BOX ---
st.markdown("""
<div class='instruction-box'>
    <b>📄 How to Use:</b><br>
    1️⃣ Choose a Village from the dropdown.<br>
    2️⃣ Enter the Khasra number in the input box.<br>
    3️⃣ Click on the <b>Search</b> button to view details.
</div>
""", unsafe_allow_html=True)

# --- VILLAGE LIST ---
villages = [
    "Ababbaspur", "Abbakaspur", "Akka Panday Bhojpur", "Asalatpur",
    "Bilari", "Bhojpur", "Chandausi", "Dilari", "Gandhupura",
    "Guladia Khurd", "Jawan", "Kanth", "Katghar", "Majhola",
    "Mau", "Mugalpura", "Nanakpur", "Pathakpur", "Rampur",
    "Sambhal", "Shahpur", "Tanda", "Usmanpur", "Zaidpur"
]

# --- USER INPUTS ---
village = st.selectbox("🏡 Select a Village", sorted(villages))
khasra = st.text_input("📜 Enter Khasra Number", placeholder="Enter valid khasra number")

# --- SEARCH ACTION ---
if st.button("Search 🔍"):
    if not khasra.strip():
        st.warning("⚠️ Please enter a Khasra number to search.")
    else:
        st.success("✅ Khasra Details Found")

        # Demo data — replace with your real database later
        df = pd.DataFrame({
            "Village": [village]*3,
            "Khasra": [khasra]*3,
            "Land use": ["Agriculture", "Residential", "Green Belt"],
            "Sub class": ["Agriculture", "Housing", "Open Space"],
            "Latitude": [28.8432, 28.8512, 28.8605],
            "Longitude": [78.7523, 78.7601, 78.7709]
        })
        st.dataframe(df, use_container_width=True)

# --- DISCLAIMER (Bilingual) ---
st.markdown("""
<div class='disclaimer'>
⚠️ <b>Disclaimer:</b> The information displayed here is for reference purposes only.  
Please verify the final land and khasra details from official records of the <b>Moradabad Development Authority</b>.<br><br>
⚠️ <b>अस्वीकरण:</b> यहाँ प्रदर्शित जानकारी केवल संदर्भ हेतु है।  
कृपया अंतिम भूमि एवं खसरा विवरण की पुष्टि <b>मुरादाबाद विकास प्राधिकरण</b> के आधिकारिक अभिलेखों से करें।
</div>
""", unsafe_allow_html=True)














