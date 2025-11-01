# app.py
import streamlit as st
import pandas as pd
from time import sleep

# ------------------- Page Config -------------------
st.set_page_config(
    page_title="Village Khasra Search Chatbot",
    page_icon="🤖",  # page_icon is OK for browser fav; UI itself won't use emojis
    layout="centered",
    initial_sidebar_state="expanded",
)

# ------------------- Load Data (unchanged logic) -------------------
@st.cache_data
def load_data():
    df = pd.read_csv("MP 2031 table_new.csv")
    # keep your exact cleaning steps
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

# ------------------- Sidebar Controls (user customization) -------------------
st.sidebar.header("Interface settings")

# Splash screen toggle
show_splash = st.sidebar.checkbox("Show opening splash screen", value=True)

# Accent color
accent = st.sidebar.selectbox("Accent color", ["Blue", "Teal", "Purple"])
accent_map = {
    "Blue": "#1E90FF",
    "Teal": "#20C997",
    "Purple": "#7C4DFF"
}
accent_color = accent_map.get(accent, "#1E90FF")

# Readability controls
font_size = st.sidebar.select_slider("Base font size", options=[14, 15, 16, 17, 18], value=16)
high_contrast = st.sidebar.checkbox("High contrast text", value=False)

# Compact layout toggle
compact = st.sidebar.checkbox("Use compact spacing", value=False)

# ------------------- CSS / Styling -------------------
bg_gradient = "linear-gradient(180deg, #0b1226 0%, #0f1724 45%, #071026 100%)"
text_color = "#FFFFFF" if not high_contrast else "#F7FBFE"
muted_color = "rgba(255,255,255,0.65)" if not high_contrast else "rgba(255,255,255,0.9)"
card_bg = "rgba(255,255,255,0.03)"
card_border = "rgba(255,255,255,0.06)"
gap = "8px" if compact else "14px"
input_height = "42px"

custom_css = f"""
<style>
:root {{
    --accent: {accent_color};
    --bg-gradient: {bg_gradient};
    --text: {text_color};
    --muted: {muted_color};
    --card-bg: {card_bg};
    --card-border: {card_border};
    --gap: {gap};
    --font-size: {font_size}px;
    --input-height: {input_height};
}}
/* Page background */
[data-testid="stAppViewContainer"] > .main {{
    background: var(--bg-gradient);
    background-attachment: fixed;
    padding: 24px;
    color: var(--text);
    font-family: "Inter", system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial;
    font-size: var(--font-size);
}}

/* Container card */
.block-container {{
    padding: 20px 22px;
    border-radius: 14px;
    background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
    box-shadow: 0 8px 30px rgba(2,6,23,0.6);
    border: 1px solid rgba(255,255,255,0.02);
}}

/* Header */
.header {{
    display:flex;
    align-items:center;
    gap: 12px;
    margin-bottom: 6px;
}}
.header .title {{
    font-weight: 700;
    font-size: 20px;
    letter-spacing: 0.2px;
}}
.header .tagline {{
    color: var(--muted);
    font-size: 13px;
    margin-top: 2px;
}}

/* layout grid */
.ui-grid {{
    display: grid;
    grid-template-columns: 360px 1fr;
    gap: 18px;
    align-items: start;
}}

/* Left card (inputs) */
.card {{
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    padding: 16px;
    border-radius: 12px;
    color: var(--text);
}}
.form-row {{
    margin-bottom: var(--gap);
}}
label {{
    display:block;
    font-size: 13px;
    color: var(--muted);
    margin-bottom: 6px;
}}

/* Inputs */
.stTextInput > div > input, .stSelectbox > div > div[role="combobox"] > div {{
    height: var(--input-height);
    padding: 8px 12px;
    background: rgba(255,255,255,0.03);
    border-radius: 8px;
    border: 1px solid rgba(255,255,255,0.04);
    color: var(--text);
}}
/* streamlit's selectbox inner text */
.stSelectbox label, .stTextInput label {{
    display:none;
}}

/* Search button */
.btn-search button {{
    height: 44px;
    background: linear-gradient(90deg, var(--accent), rgba(255,255,255,0.02));
    border: none;
    color: white;
    font-weight: 600;
    border-radius: 10px;
    padding: 0 16px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.45);
}}
.btn-search button:hover {{
    transform: translateY(-1px);
}}

/* Right side: result area */
.result-area {{
    min-height: 220px;
}}
.result-card {{
    background: linear-gradient(180deg, rgba(255,255,255,0.015), rgba(255,255,255,0.01));
    border: 1px solid rgba(255,255,255,0.03);
    padding: 18px;
    border-radius: 12px;
    box-shadow: 0 6px 20px rgba(2,6,23,0.6);
}}
.result-title {{
    display:flex;
    justify-content:space-between;
    align-items:center;
    gap:8px;
    margin-bottom: 10px;
}}
.result-title h3{{
    margin:0;
    color: var(--text);
    font-size: 15px;
}}
.result-sub {{
    color: var(--muted);
    font-size: 13px;
}}

/* Table styling (streamlit table wrapper) */
.stDataFrame > div {{
    border-radius: 10px;
    overflow: hidden;
}}
.dataframe tbody tr td {{
    color: var(--text);
    padding: 10px 12px;
    background: rgba(255,255,255,0.01);
    border-bottom: 1px solid rgba(255,255,255,0.02);
}}

/* expander style */
[data-testid="stExpander"] > div > button {{
    color: var(--text);
}}
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# ------------------- Header with inline SVG icon (no emoji in UI) -------------------
robot_svg = """
<svg width="36" height="36" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
  <rect x="3" y="7" width="18" height="12" rx="2" stroke="var(--accent)" stroke-width="1.2" fill="rgba(255,255,255,0.02)"/>
  <circle cx="8.5" cy="12.5" r="0.95" fill="var(--accent)"/>
  <circle cx="15.5" cy="12.5" r="0.95" fill="var(--accent)"/>
  <rect x="9.2" y="3.5" width="5.6" height="2.2" rx="1.1" fill="var(--accent)"/>
</svg>
"""

st.markdown('<div class="block-container">', unsafe_allow_html=True)
st.markdown(f'''
<div class="header">
  <div style="line-height:0;">{robot_svg}</div>
  <div>
    <div class="title">Village Khasra Search Chatbot</div>
    <div class="tagline">Search land records quickly — clear, readable and professional.</div>
  </div>
</div>
''', unsafe_allow_html=True)

# ------------------- Optional Splash / Intro -------------------
if show_splash:
    with st.container():
        st.markdown("""
        <div style="margin: 8px 0 16px 0;">
            <div style="padding:14px; border-radius:12px; border:1px solid rgba(255,255,255,0.02);
                        background: linear-gradient(90deg, rgba(255,255,255,0.01), rgba(255,255,255,0.005));">
                <div style="display:flex; align-items:center; gap:12px;">
                    <div style="width:56px; height:56px; border-radius:10px; background: rgba(255,255,255,0.02); display:flex; align-items:center; justify-content:center;">
                        <!-- small robot icon -->
                        <svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                          <rect x="4" y="6" width="16" height="12" rx="2" stroke="var(--accent)" stroke-width="1.0" fill="rgba(255,255,255,0.02)"/>
                          <circle cx="8.5" cy="12.5" r="0.7" fill="var(--accent)"/>
                          <circle cx="15.5" cy="12.5" r="0.7" fill="var(--accent)"/>
                        </svg>
                    </div>
                    <div>
                        <div style="font-weight:600; font-size:15px; color:var(--text);">Welcome</div>
                        <div style="color:var(--muted); font-size:13px;">Use the left panel to select village and enter Khasra number. Change accent or font size from settings.</div>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ------------------- Main two-column layout -------------------
st.markdown('<div class="ui-grid">', unsafe_allow_html=True)

# Left column: inputs
with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="form-row">', unsafe_allow_html=True)
    st.write("")  # spacer for consistent layout within container
    # Village selectbox
    village = st.selectbox("Village", options=sorted(df["Village"].unique()))
    # Khasra input
    khasra = st.text_input("Khasra number")
    st.markdown('</div>', unsafe_allow_html=True)

    # Search button
    # Put search button in an HTML wrapper to style it using CSS above
    search_col = st.columns([1, 0.2])[0]
    with search_col:
        if st.button("Search"):
            perform_search = True
        else:
            perform_search = False

    st.markdown('</div>', unsafe_allow_html=True)

# Right column: results
st.markdown('<div class="result-area">', unsafe_allow_html=True)
st.markdown('<div class="result-card">', unsafe_allow_html=True)
st.markdown('<div class="result-title">', unsafe_allow_html=True)
st.markdown('<div><h3>Search results</h3><div class="result-sub">Khasra details (Village / Khasra / Land use / Sub class / Lat / Long)</div></div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Execute search when button clicked or when user presses Enter into the input (we require explicit button here)
if perform_search and khasra:
    # mimic a short typing/processing indicator to improve UX
    with st.spinner("Checking records..."):
        sleep(0.9)

    # preserve the original filtering logic
    result = df[(df["Village"] == village) & (df["Khasra"] == khasra.strip())]

    if not result.empty:
        # Show a concise card + table
        st.markdown('<div style="margin-bottom:8px; color:var(--muted); font-size:13px;">Results found for your query</div>', unsafe_allow_html=True)
        st.dataframe(result[["Village", "Khasra", "Land use", "Sub class", "Latitude", "Longitude"]].reset_index(drop=True))
    else:
        st.markdown('<div style="padding:14px; border-radius:8px; background: rgba(255,20,60,0.02); border: 1px solid rgba(255,255,255,0.02); color:var(--muted);">No matching Khasra found for the selected village.</div>', unsafe_allow_html=True)

else:
    # initial state: helpful note
    st.markdown('<div style="color:var(--muted);">Enter a Khasra number and click "Search" to retrieve details. You can change accent color and font size in Settings.</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # close result-card
st.markdown('</div>', unsafe_allow_html=True)  # close result-area

st.markdown('</div>', unsafe_allow_html=True)  # close ui-grid
st.markdown('</div>', unsafe_allow_html=True)  # close block-container

# ------------------- Full dataset (expander) -------------------
with st.expander("View full dataset"):
    st.dataframe(df)



