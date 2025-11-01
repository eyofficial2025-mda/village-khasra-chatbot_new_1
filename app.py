import streamlit as st
import pandas as pd
from PIL import Image

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Village Khasra Chatbot", page_icon="💬", layout="wide")

# ---------- CUSTOM CSS ----------
st.markdown("""
    <style>
    body {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        color: #ffffff;
        font-family: 'Poppins', sans-serif;
    }
    .main {
        background-color: transparent;
    }
    h1 {
        text-align: center;
        color: #00f9ff;
        text-shadow: 0px 0px 10px #00f9ff;
        font-weight: 700;
    }
    .stTextInput > div > div > input {
        background-color: #222;
        color: white;
        border-radius: 8px;
        border: 1px solid #00f9ff;
    }
    .stSelectbox > div > div {
        background-color: #222;
        color: white;
        border-radius: 8px;
        border: 1px solid #00f9ff;
    }
    .stButton > button {
        background: linear-gradient(90deg, #00f9ff, #0077ff);
        color: black;
        border: none;
        border-radius: 8px;
        padding: 8px 25px;
        font-weight: bold;
        box-shadow: 0 0 15px #00f9ff;
        transition: all 0.3s ease-in-out;
    }
    .stButton > button:hover {
        transform: scale(1.1);
        background: linear-gradient(90deg, #0077ff, #00f9ff);
    }
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        padding: 25px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 0 25px rgba(0, 249, 255, 0.2);
    }
    </style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown("<h1>💬 Village Khasra Chatbot</h1>", unsafe_allow_html=True)

# ---------- SIDEBAR ----------
with st.sidebar:
    st.markdown("## 🔍 Search Khasra Details")
    village = st.selectbox("🏡 Select Village", ["Ababkaspur", "Asalatpur", "Lodhipur", "Nawada"])
    khasra = st.text_input("📜 Enter Khasra Number", "")
    if st.button("Search"):
        if khasra:
            st.session_state["khasra_result"] = f"Khasra {khasra} in {village} is under review."
            st.rerun()
        else:
            st.warning("Please enter a valid Khasra number.")

# ---------- MAIN AREA ----------
st.markdown("<br>", unsafe_allow_html=True)
col1, col2 = st.columns([3, 2])

with col1:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("💬 Chat Window")
    if "khasra_result" in st.session_state:
        st.success(st.session_state["khasra_result"])
    else:
        st.info("👋 Hello! I’m your Village Khasra Assistant. Please select your village and enter a Khasra number.")
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("📸 Village Snapshot")
    try:
        image = Image.open("village_bg.png")  # place the image file in same directory
        st.image(image, use_container_width=True)
    except:
        st.info("Upload a village image (village_bg.png) for better visualization.")
    st.markdown("</div>", unsafe_allow_html=True)

# ---------- FOOTER ----------
st.markdown("""
    <hr style="border: 1px solid #00f9ff; opacity: 0.3;">
    <p style='text-align:center; color:gray; font-size:12px;'>
    🌾 Powered by Moradabad Land Data · © 2025 MDA Digital Innovation
    </p>
""", unsafe_allow_html=True)
