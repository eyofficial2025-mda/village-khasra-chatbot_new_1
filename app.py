import streamlit as st
import pandas as pd

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

st.set_page_config(page_title="Village Khasra Bot", layout="centered")

st.markdown("""
    <style>
    body {
        background: linear-gradient(180deg, #222831, #393E46);
        color: #EEEEEE;
        font-family: 'Poppins', sans-serif;
    }
    .chat-header {
        text-align: center;
        font-size: 2.2rem;
        color: #00ADB5;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .chat-bubble {
        background: #00ADB5;
        color: #222831;
        padding: 12px;
        border-radius: 18px;
        margin: 10px 0;
        display: inline-block;
    }
    .stButton>button {
        border: none;
        background: #00ADB5;
        color: #222831;
        border-radius: 12px;
        padding: 8px 20px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background: #02C4D2;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='chat-header'>🤖 Friendly Village Khasra Bot</div>", unsafe_allow_html=True)

village = st.selectbox("🏘️ Choose a Village", sorted(df["Village"].unique()))
khasra = st.text_input("📜 Enter Khasra Number")

if khasra:
    result = df[(df["Village"] == village) & (df["Khasra"] == khasra)]
    if not result.empty:
        st.markdown("<div class='chat-bubble'>✅ Found details below:</div>", unsafe_allow_html=True)
        st.table(result[["Village", "Khasra", "Land use", "Sub class", "Latitude", "Longitude"]])
    else:
        st.markdown("<div class='chat-bubble'>⚠️ No record found.</div>", unsafe_allow_html=True)
else:
    st.info("Enter a Khasra number to start chatting.")

with st.expander("📘 Full Dataset"):
    st.dataframe(df)






