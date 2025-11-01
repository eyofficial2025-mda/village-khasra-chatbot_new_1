# app.py - robust, defensive version
import streamlit as st
import pandas as pd
import base64
import os
import traceback

# ---------- Page config ----------
st.set_page_config(page_title="Village Khasra Chatbot (Robust)", layout="centered")

# ---------- Helpers ----------
def read_csv_safe(path):
    try:
        df = pd.read_csv(path)
        # keep your exact cleaning steps
        df.columns = df.columns.str.strip().str.replace('\ufeff', '', regex=False).str.lower()
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
        return df, None
    except Exception as e:
        return None, e

def load_bg_image_as_datauri(path, max_bytes=5_000_000):
    """
    Convert image to data URI safely. If file missing or too large, return None.
    """
    if not os.path.exists(path):
        return None, f"Background image not found at: {path}"
    size = os.path.getsize(path)
    if size > max_bytes:
        return None, f"Background image is too large ({size} bytes). Try using an image < {max_bytes} bytes."
    try:
        with open(path, "rb") as f:
            data = f.read()
        encoded = base64.b64encode(data).decode()
        mime = "image/png" if path.lower().endswith(".png") else "image/jpeg"
        data_uri = f"data:{mime};base64,{encoded}"
        return data_uri, None
    except Exception as e:
        return None, e

# ---------- Paths (adjust names if different) ----------
CSV_PATH = "MP 2031 table_new.csv"
BG_IMAGE = "e9ee4e1a-cd45-4f6e-8f56-f0720150ce83.png"  # change to your filename if different

# ---------- Try to read CSV ----------
df, csv_err = read_csv_safe(CSV_PATH)
if csv_err:
    st.error("Failed to read or parse the CSV file.")
    st.markdown("**Action steps:**")
    st.markdown(f"- Make sure the CSV file is named exactly: `{CSV_PATH}` and present in the same folder as `app.py`.")
    st.markdown("- Make sure the file is a valid CSV (open it in Excel/Notepad to inspect).")
    st.markdown("- If it still fails, copy the error details below and paste them in the chat so I can debug.")
    st.exception(csv_err)
    # stop further execution to avoid cascading errors
    st.stop()

# ---------- Prepare background (safe) ----------
data_uri, bg_err = load_bg_image_as_datauri(BG_IMAGE)

if data_uri:
    css_bg = f"""
    <style>
    [data-testid="stAppViewContainer"] > .main {{
        background-image: url("{data_uri}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
        color: white !important;
    }}
    </style>
    """
else:
    # fallback dark gradient and give info (but don't expose internal error unless helpful)
    css_bg = """
    <style>
    [data-testid="stAppViewContainer"] > .main {
        background: linear-gradient(180deg, #071026 0%, #0b1226 60%, #071026 100%);
        color: white !important;
    }
    </style>
    """
    if bg_err:
        # show advice but avoid huge traceback
        st.info("Background image not applied: " + str(bg_err))

# ---------- Inject CSS (colors: blue + green theme, white text) ----------
st.markdown(css_bg, unsafe_allow_html=True)

st.markdown("""
<style>
/* font & simple resets */
:root {
  --accent-blue: #00B2FF;
  --accent-green: #00FF88;
  --muted: rgba(255,255,255,0.75);
  --card-bg: rgba(0,0,0,0.45);
}

/* main container styling */
.block-container {
  padding: 20px;
  border-radius: 14px;
}

/* headings */
h1 { color: white !important; font-weight: 700; }

/* inputs */
.stTextInput > div > input, .stSelectbox > div[role="combobox"] > div {
  background: rgba(255,255,255,0.06) !important;
  color: white !important;
  border: 1px solid rgba(255,255,255,0.06) !important;
  border-radius: 10px !important;
  padding: 10px !important;
}

/* buttons - blue -> green gradient */
.stButton > button {
  background: linear-gradient(90deg, var(--accent-blue), var(--accent-green)) !important;
  color: #001018 !important;
  font-weight: 700;
  border-radius: 10px !important;
  padding: 8px 16px !important;
}

/* dataframes / tables */
.stDataFrame, .dataframe {
  color: white !important;
  border-radius: 10px;
  overflow: hidden;
}

/* small muted */
.small-muted { color: var(--muted); font-size: 13px; }

/* accessibility toolbar styling (sidebar) */
[data-testid="stSidebar"] .css-1v0mbdj {
  background: rgba(0,0,0,0.55);
}
</style>
""", unsafe_allow_html=True)

# ---------- Accessibility controls in sidebar ----------
st.sidebar.header("Accessibility & View")
font_size = st.sidebar.slider("Base font size (px)", 12, 22, 16)
high_contrast = st.sidebar.checkbox("High contrast (white text, stronger contrast)", value=True)
reduce_motion = st.sidebar.checkbox("Reduce motion / animations", value=False)

# apply font size via inline style
st.markdown(f"<style>body{{font-size:{font_size}px;}}</style>", unsafe_allow_html=True)

if high_contrast:
    st.markdown("<style>body { color: white !important; } </style>", unsafe_allow_html=True)

# ---------- App content ----------
st.markdown("<h1 style='text-align:center;'>Village Khasra Search Chatbot</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:rgba(255,255,255,0.8);'>Blue/green theme, white text. Use sidebar to adjust accessibility.</p>", unsafe_allow_html=True)
st.markdown("---")

# input area
village = st.selectbox("Select Village", sorted(df["Village"].unique()))
khasra = st.text_input("Enter Khasra Number")

# run safe search inside try/except so we always show a helpful error
if st.button("Search"):
    try:
        if not khasra or not isinstance(khasra, str) or not khasra.strip():
            st.warning("Please enter a valid Khasra number (non-empty).")
        else:
            q = khasra.strip()
            result = df[(df["Village"] == village) & (df["Khasra"] == q)]
            if not result.empty:
                st.success("Record found — shown below:")
                st.dataframe(result[["Village", "Khasra", "Land use", "Sub class", "Latitude", "Longitude"]].reset_index(drop=True))
            else:
                st.warning("No matching Khasra found in this village.")
    except Exception as e:
        st.error("An unexpected error occurred during the search.")
        # show the traceback so you can paste it back to me
        tb = traceback.format_exc()
        st.code(tb, language="text")

# footer
st.markdown("---")
st.markdown("<div style='text-align:center; color:rgba(255,255,255,0.7);'>If this still errors, run <code>streamlit run app.py</code> in terminal and paste the full error traceback here.</div>", unsafe_allow_html=True)

