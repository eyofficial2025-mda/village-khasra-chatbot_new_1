import streamlit as st
import pandas as pd

# Load data
df = pd.read_csv("MP 2031 table_new.csv")

# Clean columns
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

# --- Streamlit Page Config ---
st.set_page_config(page_title="Village Khasra Search Chatbot", layout="centered", page_icon="🗺️")

# --- Custom CSS for Modern Look ---
st.markdown("""
    <style>
        /* Background gradient */
        body {
            background: linear-gradient(120deg, #89f7fe 0%, #66a6ff 100%);
            background-attachment: fixed;
        }
        /* Center container */
        .block-container {
            max-width: 800px;
            padding: 2rem;
            background-color: rgba(255,255,255,0.85);
            border-radius: 20px;
            box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        }
        /* Header */
        h1 {
            text-align: center;
            color: #004aad;
            text-shadow: 1px 1px 3px rgba(0,0,0,0.2);
        }
        /* Input fields */
        .stSelectbox, .stTextInput {
            background-color: white !important;
            border-radius: 10px !important;
            padding: 10px !important;
        }
        /* Buttons */
        button {
            border-radius: 12px !important;
            background-color: #004aad !important;
            color: white !important;
            font-weight: bold !important;
        }
        /* Chat-like cards */
        .chat-bubble {
            background-color: #f0f6ff;
            border-left: 5px solid #004aad;
            padding: 1rem;
            border-radius: 10px;
            margin-top: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .chat-bubble-user {
            background-color: #e1ffe1;
            border-left: 5px solid #00c853;
        }
        /* Table */
        table {
            border-radius: 10px;
            overflow: hidden;
            background: white;
        }
        /* Expander styling */
        .streamlit-expanderHeader {
            font-weight: bold;
            color: #004aad !important;
        }
    </style>
""", unsafe_allow_html=True)

# --- Title ---
st.markdown("<h1>🗺️ Village Khasra Search Chatbot</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:gray;'>Search land details with a touch of fun 🌾</p>", unsafe_allow_html=True)

# --- Inputs ---
village = st.selectbox("🏘️ Select a Village", sorted(df["Village"].unique()))
khasra = st.text_input("🔍 Enter Khasra Number")

# --- Chat-like Response ---
if khasra:
    khasra = khasra.strip()
    result = df[(df["Village"] == village) & (df["Khasra"] == khasra)]

    if not result.empty:
        st.markdown(
            f"<div class='chat-bubble-user'>💬 You searched for: <b>{khasra}</b> in <b>{village}</b></div>",
            unsafe_allow_html=True
        )
        st.markdown("<div class='chat-bubble'>✅ <b>Khasra details found!</b> Here’s what I found:</div>", unsafe_allow_html=True)
        st.table(result[["Village", "Khasra", "Land use", "Sub class", "Latitude", "Longitude"]])
    else:
        st.markdown(
            f"<div class='chat-bubble-user'>💬 You searched for: <b>{khasra}</b> in <b>{village}</b></div>",
            unsafe_allow_html=True
        )
        st.markdown("<div class='chat-bubble'>⚠️ No matching Khasra found in this village.</div>", unsafe_allow_html=True)
else:
    st.markdown("<div class='chat-bubble'>👋 Hello! Please enter a Khasra number to begin your search.</div>", unsafe_allow_html=True)

# --- Expander for Full Dataset ---
with st.expander("📘 View full dataset"):
    st.dataframe(df)

