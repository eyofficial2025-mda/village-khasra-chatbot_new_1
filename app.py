# app.py
import streamlit as st
import pandas as pd
import json
from time import sleep
from html import escape

# -------------- Page config --------------
st.set_page_config(
    page_title="Village Khasra Search — Modern UI",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------- Load CSV (unchanged logic) --------------
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

# -------------- Session state setup --------------
if "history" not in st.session_state:
    st.session_state.history = []  # list of dicts: {village, khasra, result_json}
if "last_result" not in st.session_state:
    st.session_state.last_result = None
if "reduced_motion" not in st.session_state:
    st.session_state.reduced_motion = False

# -------------- Accessibility & Theme options (sidebar) --------------
st.sidebar.header("Interface & Accessibility")
show_splash = st.sidebar.checkbox("Show animated opening splash", value=True)
theme_accent = st.sidebar.selectbox("Accent color", ["Electric Blue", "Teal", "Magenta"])
accent_map = {
    "Electric Blue": "#00B4FF",
    "Teal": "#20C997",
    "Magenta": "#D63384"
}
accent = accent_map.get(theme_accent, "#00B4FF")

font_size = st.sidebar.select_slider("Base font size", [14, 15, 16, 17, 18], value=16)
high_contrast = st.sidebar.checkbox("High contrast text", value=False)
large_buttons = st.sidebar.checkbox("Large buttons (accessible)", value=True)
reduced_motion = st.sidebar.checkbox("Reduce animations", value=False)
st.session_state.reduced_motion = reduced_motion

# -------------- small helper functions --------------
def safe_html(text):
    return escape(str(text))

def record_history(village, khasra, result_df):
    entry = {
        "village": village,
        "khasra": khasra,
        "count": len(result_df),
        "sample": result_df.head(1).to_dict(orient="records")
    }
    st.session_state.history.insert(0, entry)
    # keep only last 20
    st.session_state.history = st.session_state.history[:20]

def get_lat_lon_preview(result_df):
    # try to extract first lat/lon
    if "Latitude" in result_df.columns and "Longitude" in result_df.columns:
        try:
            r0 = result_df.iloc[0]
            lat = float(r0["Latitude"])
            lon = float(r0["Longitude"])
            if -90 <= lat <= 90 and -180 <= lon <= 180:
                return lat, lon
        except Exception:
            return None
    return None

# -------------- CSS & visuals --------------
main_css = f"""
<style>
:root {{
  --accent: {accent};
  --bg1: #071026;
  --bg2: #0b1226;
  --card: rgba(255,255,255,0.03);
  --muted: rgba(255,255,255,0.65);
  --text: #E9F0FF;
  --glass-border: rgba(255,255,255,0.035);
  --gap: 12px;
  --font-size: {font_size}px;
  --btn-radius: 12px;
  --btn-height: {'56px' if large_buttons else '44px'};
}}
/* page background */
[data-testid="stAppViewContainer"] > .main {{
  background: radial-gradient(1200px 600px at 10% 10%, rgba(0,180,255,0.04), transparent),
              linear-gradient(180deg, var(--bg1), var(--bg2));
  color: var(--text);
  font-family: Inter, ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial;
  font-size: var(--font-size);
}}
/* block container */
.block-container {{
  padding: 22px;
  border-radius: 14px;
}}

/* header */
.app-header {{
  display:flex;
  gap: 14px;
  align-items:center;
  margin-bottom: 10px;
}}
.app-title {{
  font-weight:700;
  font-size:20px;
  color: var(--text);
}}
.app-subtitle {{
  color: var(--muted);
  font-size:13px;
}}

/* layout grid */
.grid {{
  display:grid;
  grid-template-columns: 420px 1fr 360px;
  gap: 22px;
  align-items: start;
  margin-top: 12px;
}}

/* left panel - form */
.panel {{
  background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
  border-radius: 12px;
  padding: 16px;
  border: 1px solid var(--glass-border);
  min-height: 220px;
}}
.form-label {{
  color: var(--muted);
  font-size: 13px;
  margin-bottom:6px;
}}
.input-style input, .stSelectbox div[role="combobox"] > div {{
  background: rgba(255,255,255,0.02) !important;
  color: var(--text) !important;
  border-radius: 10px;
  padding: 10px 12px;
  height: 40px;
  border: 1px solid rgba(255,255,255,0.03);
}}

/* buttons */
.btn {{
  display:inline-block;
  height: var(--btn-height);
  border-radius: var(--btn-radius);
  background: linear-gradient(90deg, rgba(255,255,255,0.03), var(--accent));
  color: #071026;
  font-weight:700;
  padding: 0 18px;
  border: none;
  cursor: pointer;
  box-shadow: 0 8px 30px rgba(0,0,0,0.6);
}}
.btn:hover {{
  transform: translateY(-3px);
}}
.btn.secondary {{
  background: transparent;
  color: var(--text);
  border: 1px solid rgba(255,255,255,0.04);
}}

/* center panel results (chat-like) */
.result-panel {{
  border-radius: 12px;
  padding: 16px;
  background: linear-gradient(180deg, rgba(255,255,255,0.01), rgba(255,255,255,0.005));
  border: 1px solid rgba(255,255,255,0.02);
  min-height: 360px;
}}
.typing {{
  display:inline-block;
  height:14px;
  width:48px;
  border-radius:8px;
  background: linear-gradient(90deg, rgba(255,255,255,0.06), rgba(255,255,255,0.02));
  position: relative;
}}
.dot {{
  height:6px;
  width:6px;
  background: var(--accent);
  border-radius:50%;
  position:absolute;
  left:6px;
  top:4px;
  animation: dot 1s infinite;
}}
.dot.d2 {{ left:20px; animation-delay:0.15s; }}
.dot.d3 {{ left:34px; animation-delay:0.30s; }}
@keyframes dot {{
  0% {{ transform: translateY(0); opacity:0.2; }}
  50% {{ transform: translateY(-6px); opacity:1; }}
  100% {{ transform: translateY(0); opacity:0.2; }}
}}
/* reduce motion support */
{"@media (prefers-reduced-motion: reduce) { .dot { animation: none; } }" if reduced_motion else ""}

/* chat bubbles */
.bubble.bot {{
  background: linear-gradient(90deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
  border-left: 4px solid var(--accent);
  padding: 12px;
  border-radius: 10px;
  margin-bottom: 10px;
}}
.bubble.user {{
  background: linear-gradient(90deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
  border-right: 4px solid rgba(255,255,255,0.03);
  padding: 12px;
  border-radius: 10px;
  margin-bottom: 10px;
  text-align: right;
}}

/* right panel (history/map/export) */
.side-panel {{
  background: linear-gradient(180deg, rgba(255,255,255,0.01), rgba(255,255,255,0.005));
  padding: 14px;
  border-radius: 12px;
  border: 1px solid rgba(255,255,255,0.02);
}}
.history-item {{
  padding: 10px;
  border-radius: 10px;
  border: 1px solid rgba(255,255,255,0.02);
  margin-bottom: 10px;
  cursor: pointer;
}}
.history-item:hover {{ background: rgba(255,255,255,0.01); }}

.small-muted {{ color: var(--muted); font-size:13px; }}
</style>
"""

st.markdown(main_css, unsafe_allow_html=True)

# -------------- Animated splash (HTML component) --------------
if show_splash:
    splash_html = f"""
    <div style="display:flex; gap:14px; align-items:center; padding:12px; border-radius:12px;
                background: linear-gradient(90deg, rgba(255,255,255,0.01), rgba(255,255,255,0.005));
                border:1px solid rgba(255,255,255,0.02); margin-bottom:12px;">
      <div style="width:86px; height:86px; border-radius:16px; display:flex; align-items:center; justify-content:center;
                  background: linear-gradient(180deg, rgba(255,255,255,0.015), rgba(255,255,255,0.01));">
        <!-- animated avatar (SVG) -->
        <svg width="68" height="68" viewBox="0 0 64 64" fill="none">
          <defs>
            <linearGradient id="g" x1="0" x2="1"><stop offset="0" stop-color="{accent}"/><stop offset="1" stop-color="#6D7CFF"/></linearGradient>
          </defs>
          <rect x="6" y="10" rx="10" ry="10" width="52" height="44" fill="rgba(255,255,255,0.02)" stroke="{accent}" stroke-width="1.2"/>
          <circle cx="22" cy="30" r="3.8" fill="{accent}"/>
          <circle cx="42" cy="30" r="3.8" fill="{accent}"/>
          <rect x="26" y="8" width="12" rx="4" fill="{accent}" opacity="0.95"/>
        </svg>
      </div>
      <div>
        <div style="font-weight:700; color:var(--text); font-size:16px;">Village Khasra Search</div>
        <div style="color:var(--muted); margin-top:6px; max-width:720px;">
           Fast, accessible & customizable search UI. Use the left panel to enter village & Khasra. Map preview and history on the right.
        </div>
      </div>
    </div>
    """
    # small reduced motion consideration
    st.components.v1.html(splash_html, height=120)

# -------------- Header row --------------
st.markdown('<div class="app-header">', unsafe_allow_html=True)
st.markdown(f'<div style="width:44px; height:44px; display:flex; align-items:center; justify-content:center; border-radius:10px; background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01)); border: 1px solid rgba(255,255,255,0.02);"><svg width="26" height="26" viewBox="0 0 24 24" fill="none"><rect x="3" y="6" width="18" height="12" rx="2" stroke="{accent}" stroke-width="1.2" fill="rgba(255,255,255,0.02)"/><circle cx="8.5" cy="12.5" r="0.95" fill="{accent}"/><circle cx="15.5" cy="12.5" r="0.95" fill="{accent}"/></svg></div>', unsafe_allow_html=True)
st.markdown(f'<div><div class="app-title">Village Khasra Search Chatbot</div><div class="app-subtitle">Accessible • Fast • Professional — choose accent & controls in Settings</div></div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# -------------- Main grid (left: form, center: chat/results, right: history/map) --------------
st.markdown('<div class="grid">', unsafe_allow_html=True)

# -- Left panel: inputs --
st.markdown('<div class="panel">', unsafe_allow_html=True)
st.markdown('<div class="form-label">Select village</div>', unsafe_allow_html=True)
village = st.selectbox("", options=sorted(df["Village"].unique()), key="village_select")
st.markdown('<div class="form-label" style="margin-top:10px;">Enter Khasra number</div>', unsafe_allow_html=True)
khasra_input = st.text_input("", placeholder="Type khasra and press Enter or click Search", key="khasra_input")

# Search and controls in a horizontal layout
cols = st.columns([0.6, 0.4])
with cols[0]:
    # Search button (supports keyboard via form_submit_button below)
    search_clicked = st.button("Search", key="search_btn", help="Search the dataset for the selected village & khasra", args=None)
with cols[1]:
    clear_btn = st.button("Clear", key="clear_btn", help="Clear last search")

st.markdown('<div style="height:6px;"></div>', unsafe_allow_html=True)
st.markdown('<div class="small-muted">Accessibility</div>', unsafe_allow_html=True)
st.markdown(f'<div style="margin-top:8px;" class="small-muted">Font: {font_size}px • Accent: {theme_accent} • Buttons: {"Large" if large_buttons else "Normal"}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)  # close left panel

# If user pressed clear
if clear_btn:
    st.session_state.last_result = None

# -- Center panel: results/chat-like --
st.markdown('<div class="result-panel">', unsafe_allow_html=True)

# Behavior: support pressing Enter to trigger search
# We'll also treat the Search button press as action.
perform_search = False
# If user pressed Enter inside the text_input, Streamlit doesn't directly give event — use a small trick:
# If text input changed and user clicks Search or presses Enter (in many browsers Enter will submit the form),
# we will handle if search_clicked or if st.session_state.khasra_input_submitted (not available).
# Simpler: consider that user will click Search; provide clear instruction.

if search_clicked and st.session_state.khasra_input.strip():
    perform_search = True

if perform_search:
    qv = st.session_state.village_select
    qk = st.session_state.khasra_input.strip()
    # show user bubble
    st.markdown(f'<div class="bubble user">You searched: <strong>{safe_html(qk)}</strong> in <strong>{safe_html(qv)}</strong></div>', unsafe_allow_html=True)
    # animated typing
    st.markdown('<div class="bubble bot"><div style="display:flex;align-items:center;gap:8px;"><div class="typing"><div class="dot"></div><div class="dot d2"></div><div class="dot d3"></div></div><div class="small-muted">Looking up records…</div></div></div>', unsafe_allow_html=True)
    # small pause to simulate processing (non-blocking enough)
    if not reduced_motion:
        sleep(0.75)
    # Filter results (exact logic preserved)
    result_df = df[(df["Village"] == qv) & (df["Khasra"] == qk)]
    st.session_state.last_result = result_df
    record_history(qv, qk, result_df)
    # display outcome
    if not result_df.empty:
        st.markdown('<div class="bubble bot"><strong>Results found — preview below.</strong></div>', unsafe_allow_html=True)
        # present as a compact card
        st.dataframe(result_df[["Village", "Khasra", "Land use", "Sub class", "Latitude", "Longitude"]].reset_index(drop=True), height=220)
        # Map preview if lat/lon present
        latlon = get_lat_lon_preview(result_df)
        if latlon:
            lat, lon = latlon
            st.markdown('<div style="margin-top:12px;"><div class="small-muted">Map preview (click to view)</div></div>', unsafe_allow_html=True)
            # Streamlit's st.map expects DataFrame with lat/lon
            try:
                st.map(pd.DataFrame({"lat":[lat],"lon":[lon]}), zoom=12)
            except Exception:
                # fallback: show plain coordinates
                st.markdown(f'<div class="small-muted">Coordinates: {lat:.6f}, {lon:.6f}</div>', unsafe_allow_html=True)
        # Export button
        csv_bytes = result_df.to_csv(index=False).encode('utf-8')
        st.download_button("Download result (CSV)", data=csv_bytes, file_name=f"result_{qv}_{qk}.csv", mime="text/csv")
    else:
        st.markdown('<div class="bubble bot"><strong>No matching Khasra found for this village.</strong></div>', unsafe_allow_html=True)
        st.markdown('<div class="small-muted" style="margin-top:8px;">Try different Khasra number or check dataset for spelling/format.</div>', unsafe_allow_html=True)
else:
    # initial helpful state
    st.markdown('<div class="bubble bot"><strong>Welcome — ready to search.</strong><div class="small-muted" style="margin-top:6px;">Select a village, enter a Khasra number and press Search. Use Settings for accent, font size, and accessibility options.</div></div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # close result-panel

# -- Right panel: history / exports / quick actions --
st.markdown('<div class="side-panel">', unsafe_allow_html=True)
st.markdown('<div style="display:flex; justify-content:space-between; align-items:center;"><div style="font-weight:700;">History</div><div class="small-muted">Recent queries</div></div>', unsafe_allow_html=True)
if not st.session_state.history:
    st.markdown('<div style="margin-top:12px;" class="small-muted">No recent searches yet. Results will appear here.</div>', unsafe_allow_html=True)
else:
    # show history items
    for idx, h in enumerate(st.session_state.history):
        # clickable item (we'll render as button using a form)
        with st.form(f"hist_form_{idx}", clear_on_submit=False):
            st.markdown(f'<div class="history-item"><div style="display:flex; justify-content:space-between;"><div><strong>{safe_html(h["khasra"])}</strong><div class="small-muted">{safe_html(h["village"])}</div></div><div class="small-muted">{h["count"]} rows</div></div></div>', unsafe_allow_html=True)
            if st.form_submit_button("Load", key=f"load_{idx}"):
                # load into center as last_result and populate inputs
                st.session_state.village_select = h["village"]
                st.session_state.khasra_input = h["khasra"]
                # perform a search immediately (simulate)
                # find matching rows
                loaded_df = df[(df["Village"] == h["village"]) & (df["Khasra"] == h["khasra"])]
                st.session_state.last_result = loaded_df
                # small visual feedback
                st.experimental_rerun()

# Quick export of full dataset
st.markdown('<div style="margin-top:12px;"><div style="font-weight:700;">Dataset</div><div class="small-muted">Download entire CSV</div></div>', unsafe_allow_html=True)
st.download_button("Download full dataset", data=df.to_csv(index=False).encode('utf-8'), file_name="MP_2031_table_new.csv", mime="text/csv")

st.markdown('</div>', unsafe_allow_html=True)  # close side-panel

st.markdown('</div>', unsafe_allow_html=True)  # close grid

# -------------- Footer / credits --------------
st.markdown('<div style="margin-top:20px; color:var(--muted); font-size:13px;">Built for public access — keep CSV in the same folder. To host publicly, deploy to Streamlit Cloud or any container hosting (instructions below).</div>', unsafe_allow_html=True)

# -------------- Deployment instructions --------------
with st.expander("How to host this app (Quick)"):
    st.markdown("""
    **Option A — Streamlit Cloud (recommended)**  
    1. Push your repo to GitHub (include `app.py` and `MP 2031 table_new.csv`).  
    2. Go to https://share.streamlit.io → New app → connect repo → choose branch and `app.py`.  
    3. Deploy. The app will be publicly accessible at `https://<your-username>-<repo>.streamlit.app`.

    **Option B — Container / VPS**  
    1. Dockerize or run `streamlit run app.py --server.port $PORT` behind a reverse proxy.  
    2. Ensure the CSV is present in the working directory or use persistent storage.

    **Notes**  
    - This UI uses only inline SVG/CSS and Streamlit components — no external images, so it is portable and fast.  
    - Accessibility: Use the Settings panel to increase font size, enable high-contrast, or reduce animations (for motion sensitivity).
    """)







