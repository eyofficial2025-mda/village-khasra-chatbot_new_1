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

st.set_page_config(page_title="Village Khasra Chatbot", layout="centered")

st.markdown("""
    <style>
    body {
        background: linear-gradient(135deg, #1E1E2F, #2C2C3E);
        color: #EEE;
        font-family: 'Inter', sans-serif;
    }
    .glass {
        background: rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 20px;
        margin-top: 20px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.3);
    }
    .title {
        text-align: center;
        font-size: 2.1rem;
        font-weight: 700;
        color: #18FFFF;
        margin-bottom: 10px;
    }
    .stButton>button {
        border: none;
        background: #18FFFF;
        color: black;
        border-radius: 10px;
        padding: 8px 20px;
        font-weight: 600;
    }
    .stButton>button:hover {
        background: #00E6E6;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='title'>💬 Village Khasra Chat</div>", unsafe_allow_html=True)
st.markdown("<div class='glass'>", unsafe_allow_html=True)

village = st.selectbox("Select Village", sorted(df["Village"].unique()))
khasra = st.text_input("Enter Khasra Number")

if khasra:
    result = df[(df["Village"] == village) & (df["Khasra"] == khasra)]
    if not result.empty:
        st.success("✅ Match found")
        st.table(result[["Village", "Khasra", "Land use", "Sub class", "Latitude", "Longitude"]])
    else:
        st.warning("⚠️ No match found.")
else:
    st.info("Enter a Khasra number to begin search.")

st.markdown("</div>", unsafe_allow_html=True)

with st.expander("📘 View Full Dataset"):
    st.dataframe(df)





