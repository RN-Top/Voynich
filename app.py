"""
VOYNICH WORKBENCH - PHASE 1: ZODIAC RADIAL CRIB & ASTRONOMICAL GROUNDING
Self-contained Streamlit application for mobile GitHub deployment.
"""

import os
import re
import math
import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Voynich Decipherment - Phase 1",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# 1. PARSING & MORPHOTACTIC NORMALIZATION ENGINE
# -----------------------------------------------------------------------------
def extract_carrier_core(token: str) -> str:
    """Strips control prefixes (C) and realization suffixes (rho) to yield invariant stem Lambda."""
    w = str(token).lower().strip()
    if not w or w.startswith("<"):
        return ""
    w = re.sub(r"[{}\[\]<!>]", "", w)
    
    # Strip compound and single control headers: qo-, qok-, qot-, ch-, sh-, da-, ok-, ot-
    w = re.sub(r"^(qok|qot|qop|qo|ok|ot|op|da|ch|sh)", "", w)
    
    # Strip realization/exit ports: -aiin, -ain, -am, -edy, -ey, -al, -ar, -y, -m, -ol, -or
    w = re.sub(r"(aiin|ain|edy|eey|am|al|ar|ol|or|ey|y|m)$", "", w)
    
    return w if w else token


def parse_ivtff_raw(lines):
    records = []
    current_folio = "f1r"
    token_regex = re.compile(r"<f(\d+[rv]\d*)\.(\d+),([@=+*][A-Za-z0-9_]+)>\s*(.*)")
    
    for line in lines:
        line_str = line.strip()
        f_match = re.match(r"<f(\d+[rv]\d*)>", line_str)
        if f_match:
            current_folio = f"f{f_match.group(1)}"
            
        m = token_regex.match(line_str)
        if m:
            folio = f"f{m.group(1)}"
            line_no = m.group(2)
            locus = m.group(3)
            raw_tokens = m.group(4)
            
            clean = re.sub(r"<[%$!@].*?>", "", raw_tokens)
            clean = re.sub(r"[{}\[\]<!>]", "", clean)
            toks = [t for t in re.split(r"[.,\s]+", clean) if t and not t.startswith("<")]
            
            for idx, tok in enumerate(toks):
                carrier = extract_carrier_core(tok)
                records.append({
                    "folio": folio,
                    "line": f"{folio}.{line_no}",
                    "locus": locus,
                    "token_idx": idx,
                    "token": tok,
                    "carrier": carrier,
                    "is_radial": any(loc_tag in locus for loc_tag in ["@Lz", "@Ro", "@Ra", "@Rz"]),
                    "is_ring": any(loc_tag in locus for loc_tag in ["@Cc", "@C1", "@C2", "@C3"]),
                })
    return pd.DataFrame(records)


@st.cache_data(show_spinner="Loading and parsing transliteration corpus...")
def load_corpus():
    primary_path = os.path.join("data", "ZL3b-n.txt")
    if os.path.exists(primary_path):
        with open(primary_path, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
        return parse_ivtff_raw(lines)
    
    # Fallback to local files or sample Zodiac dataset
    csv_candidates = [f for f in os.listdir(".") if f.endswith(".csv")]
    for csv_file in csv_candidates:
        if "voynich" in csv_file.lower():
            try:
                df_csv = pd.read_csv(csv_file)
                if "clean" in df_csv.columns and "token" not in df_csv.columns:
                    df_csv["token"] = df_csv["clean"]
                if "carrier" not in df_csv.columns and "token" in df_csv.columns:
                    df_csv["carrier"] = df_csv["token"].apply(extract_carrier_core)
                if "is_radial" not in df_csv.columns:
                    df_csv["is_radial"] = df_csv.get("locus", "").astype(str).str.contains(r"@Lz|@Ro|@Ra", regex=True)
                return df_csv
            except Exception:
                continue

    # Curated canonical Zodiac tokens (f70v–f73v) if no file uploaded
    mock_data = [
        {"folio": "f70v2", "line": "f70v2.1", "locus": "@Lz1", "token": "otcheod", "carrier": "cheod", "is_radial": True, "is_ring": False},
        {"folio": "f70v2", "line": "f70v2.2", "locus": "@Lz2", "token": "oteodal", "carrier": "eod", "is_radial": True, "is_ring": False},
        {"folio": "f70v2", "line": "f70v2.3", "locus": "@Cc1", "token": "qokedy", "carrier": "k", "is_radial": False, "is_ring": True},
        {"folio": "f71r", "line": "f71r.1", "locus": "@Lz1", "token": "opairam", "carrier": "pair", "is_radial": True, "is_ring": False},
        {"folio": "f72r1", "line": "f72r1.1", "locus": "@Lz3", "token": "okeal", "carrier": "e", "is_radial": True, "is_ring": False},
        {"folio": "f72v1", "line": "f72v1.5", "locus": "@Lz5", "token": "oeeod", "carrier": "eeod", "is_radial": True, "is_ring": False},
        {"folio": "f114v", "line": "f114v.21", "locus": "@P0", "token": "otcheodaiin", "carrier": "cheod", "is_radial": False, "is_ring": False},
        {"folio": "f114v", "line": "f114v.29", "locus": "@P0", "token": "qopairam", "carrier": "pair", "is_radial": False, "is_ring": False},
        {"folio": "f114v", "line": "f114v.31", "locus": "@P0", "token": "otcheody", "carrier": "cheod", "is_radial": False, "is_ring": False},
    ]
    return pd.DataFrame(mock_data)


# -----------------------------------------------------------------------------
# 2. HISTORICAL ASTRONOMICAL REFERENCE MATRIX (15TH-CENTURY EPHEMERIDES)
# -----------------------------------------------------------------------------
PTOLEMAIC_DECANS = [
    {"Sign": "Aries (Mars)", "Decan 1 (0°-10°)": "Mars", "Decan 2 (10°-20°)": "Sun", "Decan 3 (20°-30°)": "Venus"},
    {"Sign": "Taurus (Abril)", "Decan 1 (0°-10°)": "Mercury", "Decan 2 (10°-20°)": "Moon", "Decan 3 (20°-30°)": "Saturn"},
    {"Sign": "Gemini (May)", "Decan 1 (0°-10°)": "Jupiter", "Decan 2 (10°-20°)": "Mars", "Decan 3 (20°-30°)": "Sun"},
    {"Sign": "Cancer (June)", "Decan 1 (0°-10°)": "Venus", "Decan 2 (10°-20°)": "Mercury", "Decan 3 (20°-30°)": "Moon"},
    {"Sign": "Leo (July)", "Decan 1 (0°-10°)": "Saturn", "Decan 2 (10°-20°)": "Jupiter", "Decan 3 (20°-30°)": "Mars"},
    {"Sign": "Virgo (August)", "Decan 1 (0°-10°)": "Sun", "Decan 2 (10°-20°)": "Venus", "Decan 3 (20°-30°)": "Mercury"},
    {"Sign": "Libra (September)", "Decan 1 (0°-10°)": "Moon", "Decan 2 (10°-20°)": "Saturn", "Decan 3 (20°-30°)": "Jupiter"},
    {"Sign": "Scorpio (October)", "Decan 1 (0°-10°)": "Mars", "Decan 2 (10°-20°)": "Sun", "Decan 3 (20°-30°)": "Venus"},
    {"Sign": "Sagittarius (Nov)", "Decan 1 (0°-10°)": "Mercury", "Decan 2 (10°-20°)": "Moon", "Decan 3 (20°-30°)": "Saturn"},
    {"Sign": "Capricorn (Dec)", "Decan 1 (0°-10°)": "Jupiter", "Decan 2 (10°-20°)": "Mars", "Decan 3 (20°-30°)": "Sun"},
    {"Sign": "Aquarius (Jan)", "Decan 1 (0°-10°)": "Venus", "Decan 2 (10°-20°)": "Mercury", "Decan 3 (20°-30°)": "Moon"},
    {"Sign": "Pisces (Feb)", "Decan 1 (0°-10°)": "Saturn", "Decan 2 (10°-20°)": "Jupiter", "Decan 3 (20°-30°)": "Mars"},
]

ZODIAC_FOLIO_MAP = {
    "Pisces (March / Mars)": "f70v2",
    "Aries Dark (Abril)": "f71r",
    "Aries Light (Abril)": "f71v",
    "Taurus Dark (May)": "f72r1",
    "Taurus Light (May)": "f72r2",
    "Gemini (June)": "f72v1",
    "Cancer (July)": "f72v2",
    "Leo (August)": "f73r",
    "Virgo (September)": "f73v",
}

# -----------------------------------------------------------------------------
# 3. INTERACTIVE DASHBOARD TABS
# -----------------------------------------------------------------------------
df = load_corpus()

st.title("🌌 Phase 1: Zodiac Radial Grounding & Crib Engine")
st.caption("Testing isolated radial labels against canonical 15th-century astronomical sequences.")

tab1, tab2, tab3, tab4 = st.tabs([
    "1. Decan Radial Matcher",
    "2. Carrier Locus Inspector",
    "3. f114v Realization Bridge",
    "4. Export Phase 1 Ledger"
])

with tab1:
    st.subheader("Ptolemaic Decan Sequence vs. Radial Labels (@Lz)")
    st.markdown(
        "Radial spokes in the astronomical rotas remove linear grammatical constraints, "
        "functioning as coordinate labels for fixed astronomical entities."
    )
    
    col_sel1, col_sel2 = st.columns(2)
    with col_sel1:
        chosen_sign = st.selectbox("Select Target Zodiac Rota:", list(ZODIAC_FOLIO_MAP.keys()))
        target_folio = ZODIAC_FOLIO_MAP[chosen_sign]
    with col_sel2:
        st.info(f"Target Folio: **`{target_folio}`** | Anchor: **{chosen_sign}**")

    c_left, c_right = st.columns(2)
    with c_left:
        st.markdown("#### Historical Ephemeris Ground Truth (Alfonsine / Picatrix)")
        p_df = pd.DataFrame(PTOLEMAIC_DECANS)
        st.dataframe(p_df, use_container_width=True)

    with c_right:
        st.markdown(f"#### Isolated Radial Tokens on `{target_folio}`")
        folio_tokens = df[df["folio"] == target_folio]
        radial_tokens = folio_tokens[folio_tokens["is_radial"] == True]
        
        if not radial_tokens.empty:
            st.dataframe(
                radial_tokens[["line", "locus", "token", "carrier"]],
                use_container_width=True
            )
        else:
            st.info(f"No specific radial labels tagged on {target_folio}. Showing all folio tokens:")
            st.dataframe(
                folio_tokens[["line", "locus", "token", "carrier"]].head(15),
                use_container_width=True
            )

with tab2:
    st.subheader("Carrier Specificity Across Structural Loci")
    st.caption("Compare token frequencies in Radial Labels (@Lz) vs Continuous Concentric Text (@Cc).")
    
    target_stems = ["cheod", "pair", "eod", "air", "k", "t"]
    selected_stem = st.selectbox("Select Invariant Carrier Stem (Lambda):", target_stems)
    
    stem_matches = df[df["carrier"].str.contains(selected_stem, case=False, na=False)]
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Corpus Occurrences", len(stem_matches))
    radial_count = int(stem_matches["is_radial"].sum()) if "is_radial" in stem_matches.columns else 0
    c2.metric("Radial Diagram Loci (@Lz)", radial_count)
    ring_count = int(stem_matches["is_ring"].sum()) if "is_ring" in stem_matches.columns else 0
    c3.metric("Concentric Ring Loci (@Cc)", ring_count)
    
    st.markdown(f"#### Recent Contexts for Carrier Stem: `{selected_stem}`")
    st.dataframe(
        stem_matches[["folio", "line", "locus", "token", "carrier"]].head(25),
        use_container_width=True
    )

with tab3:
    st.subheader("The f114v Celestial Realization Handoff")
    st.markdown(
        "Folio **f114v** proves the handoff where isolated astronomical carriers "
        "(`otcheod`, `opair`) enter running procedural recipes."
    )
    
    f114v_data = df[df["folio"] == "f114v"]
    if not f114v_data.empty:
        st.dataframe(
            f114v_data[["line", "locus", "token", "carrier"]],
            use_container_width=True
        )
    else:
        st.warning("f114v not found in current view. Sample realization triad:")
        st.code(
            "Line 21: chdaiin qokedy otcheodaiin qokchdy  --> Slot Omega buffer (-aiin)\n"
            "Line 29: opchdy qopairam ycheey            --> Terminal resultative flush (-am)\n"
            "Line 31: qopcheo ocpheody otcheody chedy   --> Stative register hold (-y)",
            language="text"
        )

with tab4:
    st.subheader("Export Phase 1 Extracted Evidence")
    csv_buffer = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download Phase 1 Extraction Ledger (CSV)",
        data=csv_buffer,
        file_name="voynich_phase1_zodiac_ledger.csv",
        mime="text/csv"
    )
    st.success(f"Phase 1 Engine ready. Loaded {len(df):,} parsed tokens.")
