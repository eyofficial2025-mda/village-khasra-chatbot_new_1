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
    body {
        background: radial-gradient(circle at top left, #0d0d0d, #121212, #000000);
        color: #e6e6e6;
        font-family: 'Inter', sans-serif;
    }

    h1 {
        text-align: center;
        color: #00f5d4;
        font-size: 2.3rem;
        text-shadow: 0px 0px 8px rgba(0,245,212,0.4);
        letter-spacing: 1px;
    }

    .stSelectbox, .stTextInput, .stButton button {
        border-radius: 10px !important;
        border: 1px solid #00f5d4 !important;
        background-color: rgba(30,30,30,0.9) !important;
        color: #eaeaea !important;
        transition: all 0.3s ease;
    }

    .stTextInput > div > div > input {
        color: #fff !important;
    }

    .stButton button:hover {
        background-color: #00f5d4 !important;
        color: #000 !important;
        box-shadow: 0 0 15px #00f5d4;
    }

    .result-box {
        background: rgba(25,25,25,0.8);
        border-radius: 15px;
        padding: 1rem 1.5rem;
        margin-top: 1.5rem;
        box-shadow: 0px 0px 20px rgba(0,245,212,0.1);
    }

    .footer {
        text-align: center;
        margin-top: 40px;
        font-size: 0.85rem;
        color: #aaa;
    }

    .disclaimer {
        margin-top: 25px;
        padding: 1rem;
        border-top: 1px solid rgba(0,245,212,0.2);
        color: #aaa;
        font-size: 0.85rem;
        text-align: center;
        line-height: 1.6;
    }

    /* Completely remove all blank divs/containers */
    div[data-testid="stVerticalBlock"] > div:empty {
        display: none !important;
    }
    div[data-testid="stHorizontalBlock"] > div:empty {
        display: none !important;
    }
    </style>
""", unsafe_allow_html=True)

# ------------- HEADER -------------
st.markdown("<h1>Village Khasra Chatbot 💬</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#9e9e9e;'>Search village land details with ease — clean, readable, professional.</p>", unsafe_allow_html=True)

# ------------- SEARCH AREA -------------
village = st.selectbox("🏡 Select a Village", sorted(df["Village"].unique()))
khasra = st.text_input("📜 Enter Khasra Number")

# only run search logic after clicking button
search_clicked = st.button("Search 🔍")

# ------------- DISPLAY RESULTS -------------
if search_clicked:
    khasra = khasra.strip()
    result = df[(df["Village"] == village) & (df["Khasra"] == khasra)]

    if not result.empty:
        st.markdown("<div class='result-box'>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='color:#00f5d4;'>✅ Khasra Details Found</h3>", unsafe_allow_html=True)
        st.dataframe(result[["Village", "Khasra", "Land use", "Sub class", "Latitude", "Longitude"]], hide_index=True)
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





