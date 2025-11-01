import streamlit as st
import pandas as pd
import base64

# === PAGE CONFIG ===
st.set_page_config(page_title="Village Khasra Search Chatbot", layout="centered")

# === BACKGROUND SETUP ===
def set_bg(image_file):
    with open(image_file, "rb") as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()
    bg_style = f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: url("data:image/png;base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
        color: white !important;
    }}
    [data-testid="stHeader"], [data-testid="stSidebar"] {{
        background: rgba(0,0,0,0.7);
    }}
    h1, h2, h3, p, div, label {{
        color: white !important;
    }}
    .stTextInput > div > div > input {{
        background-color: rgba(255,255,255,0.1);
        color: white !important;
        border: 1px solid #00B2FF;
        border-radius: 10px;
    }}
    .stSelectbox > div > div {{
        background-color: rgba(255,255,255,0.1);
        color: white !important;
        border: 1px solid #00B2FF;
        border-radius: 10px;
    }}
    .stButton > button {{
        background: linear-gradient(90deg, #00B2FF, #00FF88);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.6em 1.4em;
        font-weight: 600;
    }}
    .stButton > button:hover {{
        box-shadow: 0 0 10px #00FF88;
    }}
    </style>
    """
    st.markdown(bg_style, unsafe_allow_html=True)

# === SET YOUR BACKGROUND IMAGE HERE ===
set_bg("e9ee4e1a-cd45-4f6e-8f56-f0720150ce83.png")

# === LOAD DATA ===
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

# === HEADER ===
st.markdown("<h1 style='text-align:center;'>🌐 Village Khasra Search Chatbot</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Search land records quickly — with clarity, accessibility, and comfort.</p>", unsafe_allow_html=True)
st.markdown("---")

# === SIDEBAR (ACCESSIBILITY TOOLS) ===
st.sidebar.header("🧩 Accessibility Controls")
font_size = st.sidebar.slider("Font size", 12, 24, 18)
contrast_mode = st.sidebar.checkbox("High contrast mode")
language = st.sidebar.selectbox("Select Language", ["English", "Hindi"])

if contrast_mode:
    st.markdown("""
    <style>
    * {color: white !important; background-color: black !important;}
    </style>
    """, unsafe_allow_html=True)

# === SEARCH PANEL ===
st.markdown(f"<h3 style='font-size:{font_size}px;'>Search Khasra Details</h3>", unsafe_allow_html=True)
village = st.selectbox("Select Village", sorted(df["Village"].unique()))
khasra = st.text_input("Enter Khasra Number")

if st.button("Search"):
    if khasra:
        result = df[(df["Village"] == village) & (df["Khasra"] == khasra)]
        if not result.empty:
            st.success("✅ Record found!")
            st.dataframe(result[["Village", "Khasra", "Land use", "Sub class", "Latitude", "Longitude"]])
        else:
            st.warning("⚠️ No record found for this Khasra in selected village.")
    else:
        st.info("Please enter a Khasra number to search.")

# === FOOTER ===
st.markdown("---")
st.markdown(
    "<p style='text-align:center; font-size:14px;'>Designed with 💙 and ♻️ for MDA • Accessible • Multilingual • User-Friendly</p>",
    unsafe_allow_html=True,
)
