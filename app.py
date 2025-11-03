import streamlit as st
import pandas as pd

# ------------- PAGE CONFIG -------------
st.set_page_config(
    page_title="Village Khasra Chatbot",
    page_icon="💬",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ------------- LOAD DATA -------------
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

# ------------- CUSTOM STYLING -------------
st.markdown("""
    <style>
    :root {
        --accent-color: #00f5d4;
        --text-dark: #111;
        --text-light: #f2f2f2;
        --bg-dark: linear-gradient(145deg, #121212, #0a0a0a);
        --bg-light: #ffffff;
        --border-light: rgba(0,0,0,0.2);
        --border-dark: rgba(255,255,255,0.15);
    }

    /* GLOBAL LAYOUT */
    .stApp {
        background: var(--bg-dark);
        color: var(--text-light);
        font-family: 'Inter', sans-serif;
        padding: 2rem;
        border-radius: 20px;
    }

    [data-theme="light"] .stApp {
        background: var(--bg-light);
        color: var(--text-dark);
    }

    h1 {
        text-align: center;
        color: var(--accent-color);
        font-size: 2.3rem;
        text-shadow: 0px 0px 6px rgba(0,245,212,0.4);
        margin-bottom: 0.3rem;
    }

    p.subtitle {
        text-align: center;
        color: #9e9e9e;
        font-size: 1rem;
        margin-top: 0;
        margin-bottom: 1.2rem;
    }

    [data-theme="light"] p.subtitle {
        color: #333;
    }

    /* GUIDE BOX */
    .guide-text {
        text-align: center;
        color: var(--text-light);
        font-size: 1rem;
        background: rgba(255,255,255,0.05);
        padding: 0.7rem 1rem;
        border-radius: 10px;
        border: 1px solid rgba(0,245,212,0.3);
        margin-bottom: 25px;
    }

    [data-theme="light"] .guide-text {
        background: rgba(0,0,0,0.03);
        border: 1px solid rgba(0,0,0,0.15);
        color: #222;
    }

    /* INPUTS */
    .stSelectbox, .stTextInput, .stButton button {
        border-radius: 10px !important;
        border: 1px solid var(--accent-color) !important;
        background-color: rgba(30,30,30,0.9) !important;
        color: var(--text-light) !important;
        transition: all 0.3s ease;
    }

    [data-theme="light"] .stSelectbox, 
    [data-theme="light"] .stTextInput {
        background-color: #f9f9f9 !important;
        color: #111 !important;
    }

    .stButton button {
        margin-top: 10px;
        border-radius: 8px;
        padding: 0.4rem 1.2rem;
        font-weight: 600;
    }

    .stButton button:hover {
        background-color: var(--accent-color) !important;
        color: #000 !important;
        box-shadow: 0 0 12px var(--accent-color);
    }

    /* RESULT BOX */
    .result-box {
        background: rgba(25,25,25,0.85);
        border-radius: 15px;
        padding: 1rem 1.5rem;
        margin-top: 1.5rem;
        box-shadow: 0px 0px 20px rgba(0,245,212,0.1);
    }

    [data-theme="light"] .result-box {
        background: rgba(250,250,250,0.8);
        color: #000;
        box-shadow: 0px 0px 10px rgba(0,0,0,0.05);
    }

    /* FOOTER */
    .footer {
        text-align: center;
        margin-top: 40px;
        font-size: 0.85rem;
        color: #aaa;
    }

    [data-theme="light"] .footer {
        color: #555;
    }

    /* DISCLAIMER */
    .disclaimer {
        margin-top: 25px;
        padding: 1rem;
        border-top: 1px solid rgba(0,245,212,0.2);
        color: #aaa;
        font-size: 0.85rem;
        text-align: center;
        line-height: 1.6;
    }

    [data-theme="light"] .disclaimer {
        color: #444;
        border-top: 1px solid rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# ------------- HEADER -------------
st.markdown("<h1>Village Khasra Chatbot 💬</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Search village land details with ease — clean, readable, professional.</p>", unsafe_allow_html=True)

# ------------- GUIDE TEXT -------------
st.markdown("""
<div class="guide-text">
<b>📝 How to Use:</b><br>
Choose your Village from the dropdown → Enter Khasra number → Click on Search 🔍
</div>
""", unsafe_allow_html=True)

# ------------- SEARCH AREA -------------
village = st.selectbox("🏡 Select a Village", sorted(df["Village"].unique()))
khasra = st.text_input("📜 Enter Khasra Number")

if st.button("Search 🔍"):
    khasra = khasra.strip()
    result = df[(df["Village"] == village) & (df["Khasra"] == khasra)]

    if not result.empty:
        st.markdown("<div class='result-box'>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='color:#00f5d4;'>✅ Khasra Details Found</h3>", unsafe_allow_html=True)
        st.dataframe(result[["Village", "Khasra", "Land use", "Sub class", "Latitude", "Longitude"]])
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='result-box'><h4 style='color:#ff4d4d;'>⚠️ No matching Khasra found in this village.</h4></div>", unsafe_allow_html=True)

# ------------- FOOTER & DISCLAIMER -------------
st.markdown("<div class='footer'>Made with 💻 by Moradabad Development Authority</div>", unsafe_allow_html=True)

st.markdown("""
<div class='disclaimer'>
<b>Disclaimer (अस्वीकरण):</b><br>
The information provided by this online tool is intended for general guidance and preliminary verification. 
For official confirmation and clarification, please contact or visit the Moradabad Development Authority.<br><br>
इस ऑनलाइन टूल द्वारा प्रदान की गई जानकारी केवल सामान्य मार्गदर्शन और प्रारंभिक सत्यापन के लिए है। 
आधिकारिक पुष्टि और स्पष्टीकरण के लिए, कृपया मुरादाबाद विकास प्राधिकरण से संपर्क करें या कार्यालय में जाएँ।
</div>
""", unsafe_allow_html=True)

















