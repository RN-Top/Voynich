import streamlit as st
import pandas as pd
import numpy as np
import os
import re
import urllib.request
from collections import Counter

st.set_page_config(page_title="Voynich Workbench", layout="wide")

# -----------------------------------------------------------------------------
# 1. Corpus Data Ingestion & Fallbacks
# -----------------------------------------------------------------------------
DATA_PATH = "data/ZL3b-n.txt"
FALLBACK_URL = "https://www.voynich.nu/data/ZL3b-n.txt"

@st.cache_data(show_spinner="Loading and parsing Voynich corpus...")
def load_corpus():
    content = ""
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
    
    if len(content.strip()) < 500:
        try:
            req = urllib.request.Request(FALLBACK_URL, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as resp:
                content = resp.read().decode('utf-8', errors='ignore')
        except Exception:
            pass

    rows = []
    current_folio = "f1r"
    current_section = "Herbal"
    
    for raw_line in content.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        
        # Detect folio headers
        m_folio = re.match(r"^<f(\d+[rv]\d?)>", line)
        if m_folio:
            current_folio = "f" + m_folio.group(1)
            num = int(re.sub(r"[^\d]", "", current_folio))
            if num <= 66:
                current_section = "Herbal"
            elif 67 <= num <= 74:
                current_section = "Astronomical"
            elif 75 <= num <= 84:
                current_section = "Biological"
            else:
                current_section = "Stars"
            continue
            
        parts = line.split(">")
        header = parts[0].strip("<>") if len(parts) > 1 else "line"
        text_part = parts[-1]
        
        words = re.split(r"[.,\s]+", text_part)
        for w in words:
            clean = re.sub(r"[^a-z0-9]", "", w.lower())
            if clean:
                state = "P"
                if clean.endswith(("ey", "eey", "edy", "eedy")):
                    state = "C"
                elif clean.endswith(("ain", "aiin", "or", "ar")):
                    state = "L"
                elif clean.endswith(("am", "m")):
                    state = "R"
                
                carrier = re.sub(r"^(q|k|d)", "", clean)
                carrier = re.sub(r"(y|ar|al|aiin|am|m)$", "", carrier)
                
                rows.append({
                    "folio": current_folio,
                    "section": current_section,
                    "header": header,
                    "clean": clean,
                    "state": state,
                    "carrier": carrier if carrier else clean
                })
                
    if not rows:
        # Fallback rows to prevent any empty crash
        for tok in ["fachys", "ykal", "ar", "ataiin", "shol", "daiin", "chedy", "qokedy", "chdam"]:
            rows.append({
                "folio": "f1r", "section": "Herbal", "header": "f1r.1",
                "clean": tok, "state": "P", "carrier": tok
            })
            
    return pd.DataFrame(rows)

df = load_corpus()

# -----------------------------------------------------------------------------
# 2. UI Layout & Tools
# -----------------------------------------------------------------------------
st.title("Voynich Manuscript Decipherment & State-Space Engine")
st.caption(f"Loaded: {len(df):,} tokens across {df['folio'].nunique()} folios.")

tabs = st.tabs([
    "1. Parallel Reader", 
    "2. Author & Colophon Audit", 
    "3. Zodiac Grounding", 
    "4. Structure & Null Tests",
    "5. Export Full Data"
])

# Tab 1: Reader
with tabs[0]:
    st.subheader("Manuscript Folio Explorer")
    folios = sorted(df["folio"].unique())
    selected_folio = st.selectbox("Select Folio:", folios, index=0)
    f_data = df[df["folio"] == selected_folio]
    
    st.markdown(f"**Folio Section:** `{f_data['section'].iloc[0]}` | **Token Count:** `{len(f_data)}`")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("#### Surface Token Stream")
        for h, grp in f_data.groupby("header", sort=False):
            line_str = " ".join(grp["clean"])
            st.text(f"{h}: {line_str}")
    with col2:
        st.markdown("#### Macrostate Sequence (C / L / P / R)")
        color_map = {"C": "#FF9999", "L": "#99CCFF", "P": "#99FF99", "R": "#FFCC99"}
        for h, grp in f_data.groupby("header", sort=False):
            html = " ".join([f"<span style='background-color:{color_map.get(s, '#EEE')}; padding:2px 4px; border-radius:3px;'>{t}</span>" for t, s in zip(grp["clean"], grp["state"])])
            st.markdown(f"**{h}:** {html}", unsafe_allow_html=True)

# Tab 2: Author Audit
with tabs[1]:
    st.subheader("Author Loci & Sign-Off Audits")
    st.markdown("Targets: `ydaraishy` (f1r.6), `ytchas` (f9r.10), `oror.sheey`")
    targets = ["ydaraishy", "ytchas", "oror"]
    matches = df[df["clean"].str.contains("|".join(targets), case=False, na=False)]
    if not matches.empty:
        st.dataframe(matches[["folio", "header", "clean", "state", "section"]], use_container_width=True)
    else:
        st.info("No colophon singletons detected in the currently parsed slice.")

# Tab 3: Zodiac Grounding
with tabs[2]:
    st.subheader("Astronomical Carrier Grounding (f67r - f74v)")
    astro_df = df[df["section"] == "Astronomical"]
    if not astro_df.empty:
        top_carriers = astro_df["carrier"].value_counts().head(15).reset_index()
        top_carriers.columns = ["Carrier Root", "Astronomical Count"]
        st.dataframe(top_carriers, use_container_width=True)
    else:
        st.info("No astronomical section tokens loaded.")

# Tab 4: Structure Tests
with tabs[3]:
    st.subheader("Empirical State Transition & Buffer Tests")
    st.markdown("**Terminal -m Buffer Flush Rate:**")
    m_tokens = df[df["clean"].str.endswith("m")]
    st.metric("Total Tokens Ending in -m", f"{len(m_tokens):,}")
    
    st.markdown("**Top Invariant Carrier Cores Across Whole Manuscript:**")
    st.dataframe(df["carrier"].value_counts().head(20).reset_index().rename(columns={"index": "Carrier", "carrier": "Count"}), use_container_width=True)

# Tab 5: Export Data
with tabs[4]:
    st.subheader("Export Processed Token Dataset")
    csv_bytes = df.to_csv(index=False).encode("utf-8")
    st.download_button("Download Processed Corpus CSV", data=csv_bytes, file_name="voynich_processed_tokens.csv", mime="text/csv")
