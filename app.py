import streamlit as st
import pandas as pd

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Village Khasra Chatbot",
    page_icon="💬",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- LOAD DATA ---
df = pd.read_csv("MP 2031 table_new.csv")
df.columns = df.columns.str.strip().str.replace('\ufeff', '').str.lower()
df = df.rename(columns={
    'village': 'Village',
    'khasra': 'Khasra',
    'land use': 'Land use',
    'sub class': 'Sub class',
    'latitude': 'Latitude',
    'longitude': 'Longitude'
})
df["Village"] = df["Village"].astype(str).str.strip()
df["Khasra"] = df["Khasra"].astype(str).str.strip()

# --- UNIVERSAL CSS ---
st.markdown("""
    <style>
    body {
        font-family: 'Inter', sans-serif;
    }

    html[data-theme="light"] body {
        background: radial-gradient(circle at top left, #f4f4f4, #e9e9e9);
        color: #111 !important;
    }
    html[data-theme="dark"] body {
        background: radial-gradient(circle at top left, #0d0d0d, #121212, #000000);
        color: #e6e6e6 !important;
    }

    h1 {
        text-align: center;
        color: #00f5d4;
        font-size: 2.3rem;
        text-shadow: 0px 0px 8px rgba(0,245,212,0.4);
        letter-spacing: 1px;
    }

    /* Guide section */
    .guide-box {
        text-align: center;
        background: rgba(255,255,255,0.6);
        border-radius: 12px;
        padding: 1rem;
        margin: 1.5rem 0;
        color: #000;
        font-size: 1rem;
        line-height: 1.6;
        box-shadow: 0px 0px 15px rgba(0,245,212,0.15);
    }
    html[data-theme="dark"] .guide-box {
        background: rgba(20,20,20,0.8);
        color: #eaeaea;
    }

    /* Input and select styling */
    .stSelectbox, .stTextInput {
        border-radius: 10px !important;
        border: 1px solid #00f5d4 !important;
        background-color: rgba(255,255,255,0.85) !important;
        color: #000 !important;
    }
    html[data-theme="dark"] .stSelectbox, 
    html[data-theme="dark"] .stTextInput {
        background-color: rgba(30,30,30,0.9) !important;
        color: #eaeaea !important;
    }

    /* Buttons */
    .stButton button {
        border-radius: 10px !important;
        border: 1px solid #00f5d4 !important;
        background: linear-gradient(135deg, #00f5d4, #00aaff);
        color: #000 !important;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton button:hover {
        box-shadow: 0 0 15px #00f5d4;
        transform: scale(1.02);
    }

    /* Result Box */
    .result-box {
        background: rgba(25,25,25,0.8);
        border-radius: 15px;
        padding: 1rem 1.5rem;
        margin-top: 1.5rem;
        box-shadow: 0px 0px 20px rgba(0,245,212,0.1);
    }
    html[data-theme="light"] .result-box {
        background: rgba(255,255,255,0.9);
        box-shadow: 0px 0px 20px rgba(0,0,0,0.1);
    }

    /* Remove phantom block */
    div[data-testid="stVerticalBlock"] > div:empty {
        display: none !important;
    }

    /* Table readability */
    .stDataFrame {
        border-radius: 10px !important;
        overflow: hidden !important;
    }

    /* Footer and disclaimer */
    .footer {
        text-align: center;
        margin-top: 40px;
        font-size: 0.85rem;
        color: #888;
    }
    .disclaimer {
        margin-top: 25px;
        padding: 1rem;
        border-top: 1px solid rgba(0,245,212,0.2);
        color: #888;
        font-size: 0.85rem;
        text-align: center;
        line-height: 1.6;
    }
    </style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown("<h1>Village Khasra Chatbot 💬</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#777;'>Search village land details with ease — clean, readable, professional.</p>", unsafe_allow_html=True)

# --- GUIDE SECTION ---
st.markdown("""
<div class='guide-box'>
<b>📝 How to Use:</b><br>
1️⃣ Choose a Village from the dropdown.<br>
2️⃣ Enter the Khasra number in the input box.<br>
3️⃣ Click on the <b>Search</b> button to view details.
</div>
""", unsafe_allow_html=True)

# --- INPUT SECTION ---
village = st.selectbox("🏡 Select a Village", sorted(df["Village"].unique()))
khasra = st.text_input("📜 Enter Khasra Number")
search_btn = st.button("Search 🔍")

# --- SINGLE PLACEHOLDER ---
placeholder = st.empty()

if search_btn:
    placeholder.empty()
    khasra = khasra.strip()
    result = df[(df["Village"] == village) & (df["Khasra"] == khasra)]

    with placeholder.container():
        if not result.empty:
            st.markdown("<div class='result-box'>", unsafe_allow_html=True)
            st.markdown("<h3 style='color:#00c896;'>✅ Khasra Details Found</h3>", unsafe_allow_html=True)
            st.dataframe(result[["Village", "Khasra", "Land use", "Sub class", "Latitude", "Longitude"]], hide_index=True)
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='result-box'><h4 style='color:#ff4d4d;'>⚠️ No matching Khasra found in this village.</h4></div>", unsafe_allow_html=True)

# --- FOOTER + DISCLAIMER ---
st.markdown("<div class='footer'>Made with 💻 by Moradabad Development Authority</div>", unsafe_allow_html=True)
st.markdown("""
<div class='disclaimer'>
<b>Disclaimer (अस्वीकरण):</b><br>
This tool provides general land-use details for reference. For verified records, please visit the Moradabad Development Authority.<br><br>
यह टूल केवल सामान्य भूमि उपयोग विवरण दिखाने के लिए है। आधिकारिक अभिलेखों हेतु कृपया मुरादाबाद विकास प्राधिकरण कार्यालय में संपर्क करें।
</div>
""", unsafe_allow_html=True)






