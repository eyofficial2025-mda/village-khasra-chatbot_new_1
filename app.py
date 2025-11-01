import streamlit as st
import pandas as pd
from time import sleep

# ------------------- Page Config -------------------
st.set_page_config(page_title="Village Khasra Search Chatbot", page_icon="🤖", layout="centered")

# ------------------- Load Data -------------------
@st.cache_data
def load_data():
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
    return df

df = load_data()

# ------------------- Sidebar (Theme & Settings) -------------------
st.sidebar.title("⚙️ Settings")

theme = st.sidebar.radio("Choose Theme:", ["Light", "Dark", "Ocean", "Sunset"])
primary_color = "#004aad"

if theme == "Light":
    bg_color = "#f9f9f9"
    bubble_user = "#e1ffe1"
    bubble_bot = "#f0f6ff"
    text_color = "#000"
elif theme == "Dark":
    bg_color = "#111827"
    bubble_user = "#1f2937"
    bubble_bot = "#374151"
    text_color = "#f3f4f6"
elif theme == "Ocean":
    bg_color = "linear-gradient(120deg, #89f7fe 0%, #66a6ff 100%)"
    bubble_user = "rgba(255,255,255,0.8)"
    bubble_bot = "rgba(255,255,255,0.65)"
    text_color = "#004aad"
elif theme == "Sunset":
    bg_color = "linear-gradient(135deg, #ff9a9e 0%, #fad0c4 100%)"
    bubble_user = "rgba(255,255,255,0.85)"
    bubble_bot = "rgba(255,255,255,0.7)"
    text_color = "#3b0a45"

# ------------------- Custom CSS -------------------
st.markdown(f"""
    <style>
    body {{
        background: {bg_color};
        color: {text_color};
    }}
    .block-container {{
        padding: 2rem;
        border-radius: 18px;
        backdrop-filter: blur(10px);
    }}
    h1 {{
        text-align: center;
        color: {primary_color};
    }}
    .chat-bubble {{
        padding: 1rem;
        border-radius: 14px;
        margin: 8px 0;
        box-shadow: 0 3px 8px rgba(0,0,0,0.1);
    }}
    .bot {{
        background: {bubble_bot};
        text-align: left;
    }}
    .user {{
        background: {bubble_user};
        text-align: right;
    }}
    .fade-in {{
        animation: fadeIn 1s ease-in;
    }}
    @keyframes fadeIn {{
        from {{opacity: 0; transform: translateY(10px);}}
        to {{opacity: 1; transform: translateY(0); opacity: 1;}}
    }}
    </style>
""", unsafe_allow_html=True)

# ------------------- Interactive Splash Screen -------------------
with st.expander("🌟 Play with Opening Screen", expanded=False):
    st.write("Welcome to the Village Khasra Search Chatbot!")
    st.write("Try changing the theme in the sidebar to match your comfort 🌗")

# ------------------- Main Title -------------------
st.markdown("<h1 class='fade-in'>🤖 Village Khasra Search Chatbot</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:gray;'>Search land records intelligently and interactively.</p>", unsafe_allow_html=True)

# ------------------- Chat Interface -------------------
village = st.selectbox("🏘️ Select a Village", sorted(df["Village"].unique()))
khasra = st.text_input("🔍 Enter Khasra Number")

if khasra:
    khasra = khasra.strip()
    result = df[(df["Village"] == village) & (df["Khasra"] == khasra)]

    # Simulate a short "typing" animation
    with st.spinner("🤖 Bot is checking records..."):
        sleep(1.2)

    if not result.empty:
        st.markdown(f"<div class='chat-bubble user'>You: Search for <b>{khasra}</b> in <b>{village}</b></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='chat-bubble bot fade-in'>✅ Khasra found! Here are the details 👇</div>", unsafe_allow_html=True)
        st.table(result[["Village", "Khasra", "Land use", "Sub class", "Latitude", "Longitude"]])
    else:
        st.markdown(f"<div class='chat-bubble user'>You: Search for <b>{khasra}</b> in <b>{village}</b></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='chat-bubble bot fade-in'>⚠️ No matching Khasra found in this village.</div>", unsafe_allow_html=True)
else:
    st.markdown(f"<div class='chat-bubble bot fade-in'>👋 Hello! Please enter a Khasra number to begin.</div>", unsafe_allow_html=True)

# ------------------- Full Dataset View -------------------
with st.expander("📘 View full dataset"):
    st.dataframe(df)


