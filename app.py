import streamlit as st
import pandas as pd

# Page Configuration
st.set_page_config(page_title="Village Khasra Chatbot", layout="centered")

# Custom CSS for universal light/dark theme styling
st.markdown("""
<style>
:root {
  --card-bg: rgba(240, 240, 240, 0.9);
  --text-color: #000;
}

[data-theme="dark"] {
  --card-bg: rgba(20, 20, 20, 0.8);
  --text-color: #fff;
}

body, .stApp {
  background: linear-gradient(145deg, #0f2027, #203a43, #2c5364);
  color: var(--text-color);
}

.title {
  text-align: center;
  font-size: 3rem;
  font-weight: 800;
  color: #00eaff;
  text-shadow: 0px 0px 20px #00eaffaa;
  margin-bottom: 0.3em;
}

.subtitle {
  text-align: center;
  font-size: 1.1rem;
  color: #bbb;
  margin-bottom: 2em;
}

.card {
  background: var(--card-bg);
  border-radius: 20px;
  padding: 25px;
  margin-bottom: 1.5em;
  box-shadow: 0 0 20px rgba(0,0,0,0.2);
  transition: transform 0.2s ease-in-out;
}
.card:hover {
  transform: scale(1.01);
}

.guide-title {
  font-weight: 700;
  font-size: 1.2rem;
  text-align: center;
  margin-bottom: 10px;
  color: #00eaff;
}

.guide-steps {
  font-size: 1rem;
  line-height: 1.7;
  text-align: left;
  margin-left: 1em;
  color: var(--text-color);
}

.disclaimer {
  font-size: 0.95rem;
  background: rgba(255, 255, 255, 0.08);
  padding: 15px;
  border-left: 5px solid #00eaff;
  border-radius: 10px;
  margin-top: 2em;
  color: var(--text-color);
}

.stSelectbox, .stTextInput > div > div > input {
  border-radius: 12px !important;
  border: 1px solid #00eaff !important;
  background-color: rgba(255,255,255,0.05) !important;
  color: var(--text-color) !important;
}

.stButton > button {
  background: linear-gradient(90deg, #00c6ff, #0072ff);
  color: white;
  border: none;
  border-radius: 10px;
  padding: 10px 24px;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
}
.stButton > button:hover {
  transform: scale(1.05);
  box-shadow: 0 0 15px #00eaffaa;
}
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<div class="title">Village Khasra Chatbot</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Search village land details with ease — clean, readable, professional.</div>', unsafe_allow_html=True)

# Guide Box
st.markdown("""
<div class="card">
  <div class="guide-title">How to Use</div>
  <div class="guide-steps">
  1️⃣ Choose a village from the dropdown.<br>
  2️⃣ Enter the Khasra number in the input box.<br>
  3️⃣ Click on the <b>Search</b> button to view details.
  </div>
</div>
""", unsafe_allow_html=True)

# Interactive Inputs
villages = ["Ababbaspur", "Kailam", "Chhapra", "Sonta", "Asalatpur"]
village = st.selectbox("Select a Village", villages)
khasra = st.text_input("Enter Khasra Number")

if st.button("Search"):
    if khasra.strip():
        st.success(f"Searching Khasra number {khasra} in {village}...")
    else:
        st.warning("Please enter a valid Khasra number before searching.")

# Disclaimer
st.markdown("""
<div class="disclaimer">
<b>Disclaimer:</b><br>
All information provided here is for reference and convenience only. Actual land records should be verified through official government sources.<br><br>
<b>अस्वीकरण:</b><br>
यह जानकारी केवल संदर्भ और सुविधा के लिए है। वास्तविक भूमि अभिलेखों की पुष्टि सरकारी अभिलेखों से अवश्य करें।
</div>
""", unsafe_allow_html=True)











