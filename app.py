import streamlit as st
import pandas as pd

st.set_page_config(page_title="Village Khasra Chatbot", page_icon="💬", layout="centered")

# --- UNIVERSAL THEME-AWARE CSS ---
st.markdown("""
    <style>
    /* Background gradient */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, var(--background-color), var(--secondary-background-color));
        color: var(--text-color);
    }

    /* Typography and readability */
    h1, h2, h3, h4, h5, h6, p, label, span, div {
        color: var(--text-color);
    }

    /* Input fields styling */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > div {
        color: var(--text-color) !important;
        background-color: var(--background-color) !important;
        border: 1px solid rgba(128, 128, 128, 0.4) !important;
        border-radius: 8px !important;
    }

    /* Placeholder text */
    ::placeholder {
        color: rgba(128, 128, 128, 0.8);
    }

    /* Primary button gradient */
    button[kind="primary"] {
        background: linear-gradient(90deg, #00C6FF, #0072FF);
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: bold;
    }

    /* Instruction box */
    .instruction-box {
        background-color: rgba(128,128,128,0.2);
        padding: 1.2rem;
        border-radius: 12px;
        margin-bottom: 1rem;
    }

    /* Disclaimer box */
    .disclaimer {
        font-size: 0.9rem;
        color: var(--text-color);
        opacity: 0.8;
        text-align: center;
        margin-top: 2.2rem;
        padding: 0.8rem;
        border-top: 1px solid rgba(128,128,128,0.3);
        line-height: 1.5;
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


# --- USER INPUTS ---
village = st.selectbox("🏡 Select a Village", ["Ababbaspur", "Mau", "Bilari"])
khasra = st.text_input("📜 Enter Khasra Number")

# --- SEARCH ACTION ---
if st.button("Search 🔍"):
    if khasra.strip() == "":
        st.warning("⚠️ Please enter a Khasra number to search.")
    else:
        st.success("✅ Khasra Details Found")
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
⚠️ <b>Disclaimer:</b> The information displayed here is for reference purposes only.  
Please verify the final land and khasra details from official records of the <b>Moradabad Development Authority</b>.<br><br>
⚠️ <b>अस्वीकरण:</b> यहाँ प्रदर्शित जानकारी केवल संदर्भ हेतु है।  
कृपया अंतिम भूमि एवं खसरा विवरण की पुष्टि <b>मुरादाबाद विकास प्राधिकरण</b> के आधिकारिक अभिलेखों से करें।
</div>
""", unsafe_allow_html=True)












