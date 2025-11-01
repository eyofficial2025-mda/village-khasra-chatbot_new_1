import streamlit as st
import pandas as pd
import time
import random

# -----------------------------------------------------
# PAGE CONFIG
# -----------------------------------------------------
st.set_page_config(
    page_title="Village Khasra Chatbot",
    page_icon="💬",
    layout="wide"
)

# -----------------------------------------------------
# CUSTOM CSS STYLING
# -----------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');

body {
    font-family: 'Poppins', sans-serif;
    background: radial-gradient(circle at top left, #0a0f1e, #091234 50%, #041029 100%);
    color: #fff;
}
h1 {
    text-align: center;
    color: #00e1ff;
    text-shadow: 0 0 15px #00e1ff;
    font-weight: 700;
    margin-top: -20px;
}
[data-testid="stSidebar"] {
    background: rgba(10, 15, 30, 0.85);
    color: #fff;
}
.chat-container {
    background: rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 20px;
    height: 520px;
    overflow-y: auto;
    box-shadow: 0 4px 20px rgba(0,0,0,0.5);
}
.user-msg {
    background: linear-gradient(90deg, #0078ff, #00e1ff);
    color: #000;
    padding: 10px 14px;
    border-radius: 15px;
    margin: 8px 0;
    text-align: right;
}
.bot-msg {
    background: rgba(255,255,255,0.12);
    border-left: 4px solid #00e1ff;
    padding: 10px 14px;
    border-radius: 15px;
    margin: 8px 0;
    text-align: left;
}
.stButton>button {
    background: linear-gradient(90deg, #00e1ff, #00ff9d);
    color: #001018 !important;
    font-weight: bold;
    border: none;
    border-radius: 10px;
    padding: 10px 22px;
    transition: 0.3s;
}
.stButton>button:hover {
    transform: scale(1.05);
    box-shadow: 0 0 15px #00ffcc;
}
.typing {
    color: #00ffcc;
    font-style: italic;
    font-size: 14px;
}
.voice-btn {
    border-radius: 50%;
    width: 48px;
    height: 48px;
    background: linear-gradient(45deg, #00ffcc, #00e1ff);
    border: none;
    color: #001018;
    font-weight: bold;
    cursor: pointer;
}
.voice-btn:hover {
    transform: scale(1.1);
    box-shadow: 0 0 20px #00e1ff;
}
.footer {
    text-align: center;
    color: rgba(255,255,255,0.6);
    margin-top: 30px;
    font-size: 13px;
}
@media (max-width: 768px) {
    .chat-container {
        height: 400px;
    }
}
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------
# LOAD DATA
# -----------------------------------------------------
try:
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
except Exception:
    st.error("⚠️ CSV file not found or unreadable. Please upload 'MP 2031 table_new.csv'.")
    st.stop()

# -----------------------------------------------------
# SESSION STATE INIT
# -----------------------------------------------------
if "chat" not in st.session_state:
    st.session_state.chat = [("bot", "👋 Hello! I’m your Village Khasra Assistant. Please select your village and enter Khasra number.")]
if "typing" not in st.session_state:
    st.session_state.typing = False

# -----------------------------------------------------
# MAIN INTERFACE
# -----------------------------------------------------
st.markdown("<h1>Village Khasra Chatbot 💬</h1>", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

# --------- CHAT SECTION ---------
with col1:
    chat_area = st.container()
    with chat_area:
        st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
        for sender, msg in st.session_state.chat:
            if sender == "user":
                st.markdown(f"<div class='user-msg'>{msg}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='bot-msg'>{msg}</div>", unsafe_allow_html=True)
        if st.session_state.typing:
            st.markdown("<div class='typing'>Bot is typing...</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# --------- SEARCH INPUT SECTION ---------
with col2:
    st.markdown("### 🔍 Search Khasra Details")
    village = st.selectbox("🏘️ Select Village", sorted(df["Village"].unique()))
    khasra = st.text_input("🧾 Enter Khasra Number")

    # Voice input placeholder (Browser API not native in Streamlit yet)
    st.markdown("<button class='voice-btn'>🎤</button> <small style='color:rgba(255,255,255,0.6)'>Voice search coming soon</small>", unsafe_allow_html=True)

    if st.button("Search"):
        if khasra:
            khasra = khasra.strip()
            st.session_state.chat.append(("user", f"Village: {village}, Khasra: {khasra}"))
            st.session_state.typing = True
            st.experimental_rerun()

# -----------------------------------------------------
# BOT RESPONSE (after rerun)
# -----------------------------------------------------
if st.session_state.typing:
    time.sleep(1.2)
    result = df[(df["Village"] == village) & (df["Khasra"] == khasra)]
    if not result.empty:
        response = f"✅ Record found for **{khasra}** in *{village}*.\nLand use: {result.iloc[0]['Land use']}, Sub-class: {result.iloc[0]['Sub class']}."
    else:
        response = f"⚠️ No record found for Khasra **{khasra}** in *{village}*."
    st.session_state.chat.append(("bot", response))
    st.session_state.typing = False
    st.experimental_rerun()

# -----------------------------------------------------
# FOOTER
# -----------------------------------------------------
st.markdown("<div class='footer'>© 2025 MDA | Designed with 💚 Blue–Green Theme for Public Accessibility</div>", unsafe_allow_html=True)
