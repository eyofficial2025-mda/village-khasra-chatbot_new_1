import streamlit as st
import pandas as pd

# Load CSV
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

# Streamlit settings
st.set_page_config(page_title="Village Khasra Search Chatbot", layout="centered")

# Custom futuristic CSS
st.markdown("""
    <style>
    body {
        background: radial-gradient(circle at 10% 20%, #0b0f1f, #141a32 90%);
        color: #E0E0E0;
        font-family: 'Poppins', sans-serif;
    }
    .main-title {
        text-align: center;
        font-size: 2.2rem;
        font-weight: 700;
        color: #00B4FF;
        text-shadow: 0px 0px 15px #00B4FF;
        margin-bottom: 20px;
    }
    .stSelectbox, .stTextInput {
        background: rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 10px;
        color: #FFF;
    }
    .stButton>button {
        background: linear-gradient(90deg, #00B4FF, #8A2BE2);
        border: none;
        border-radius: 20px;
        color: white;
        font-weight: bold;
        padding: 8px 20px;
        box-shadow: 0 0 10px #00B4FF;
        transition: 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 25px #8A2BE2;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='main-title'>🤖 Village Khasra Search Chatbot</div>", unsafe_allow_html=True)

village = st.selectbox("🏡 Select a Village", sorted(df["Village"].unique()))
khasra = st.text_input("🔍 Enter Khasra Number")

if khasra:
    khasra = khasra.strip()
    result = df[(df["Village"] == village) & (df["Khasra"] == khasra)]
    if not result.empty:
        st.success("✅ Khasra details found:")
        st.table(result[["Village", "Khasra", "Land use", "Sub class", "Latitude", "Longitude"]])
    else:
        st.warning("⚠️ No matching Khasra found in this village.")
else:
    st.info("Enter a Khasra number to begin the search.")

with st.expander("📘 View full dataset"):
    st.dataframe(df)




