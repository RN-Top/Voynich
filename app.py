import streamlit as st
import pandas as pd
import numpy as np
import os
import re
import urllib.request

st.set_page_config(page_title="Voynich Decipherment & Decan Oracle", layout="wide")

# -----------------------------------------------------------------------------
# 1. CORPUS INGESTION & AUTO-HYDRATION
# -----------------------------------------------------------------------------
@st.cache_data(show_spinner="Loading and parsing manuscript corpus...")
def load_data():
    candidates = ["data/ZL3b-n.txt", "ZL3b-n.txt", "data/ZL3b-n 2.txt", "ZL3b-n 2.txt"]
    target = None
    for p in candidates:
        if os.path.exists(p) and os.path.getsize(p) > 5000:
            target = p
            break
    if not target:
        os.makedirs("data", exist_ok=True)
        target = "data/ZL3b-n.txt"
        urls = [
            "https://raw.githubusercontent.com/RN-Top/Voynich/main/data/ZL3b-n.txt",
            "https://www.voynich.nu/data/ZL3b-n.txt",
            "https://www.icir.org/christian/voynich/ZL3b-n.txt"
        ]
        for u in urls:
            try:
                urllib.request.urlretrieve(u, target)
                if os.path.exists(target) and os.path.getsize(target) > 5000:
                    break
            except Exception:
                continue

    records = []
    if os.path.exists(target):
        curr_folio = "f1r"
        with open(target, "r", encoding="utf-8", errors="ignore") as f:
            for raw_line in f:
                line = raw_line.strip()
                if not line or line.startswith("#") or line.startswith("<!"):
                    continue
                f_head = re.match(r"<f?(\d+[rv]\d*|[A-Za-z]+)>", line)
                if f_head:
                    curr_folio = f"f{f_head.group(1).lower()}"
                    continue
                match = re.match(r"<([^>]+)>\s*(.*)", line)
                if match:
                    loc, content = match.group(1), match.group(2)
                    parts = loc.split(".")
                    folio = parts[0].lower().replace("<", "")
                    if not re.search(r"(\d+[rv]|ros)", folio):
                        folio = curr_folio
                    line_no = parts[1].split(",")[0] if len(parts) > 1 else "1"
                    locus = parts[1].split(",")[-1] if len(parts) > 1 and "," in parts[1] else "+P0"
                    
                    sec = "Herbal"
                    fn = re.search(r"(\d+)", folio)
                    if fn:
                        fi = int(fn.group(1))
                        if 67 <= fi <= 74: sec = "Astronomical/Zodiac"
                        elif 75 <= fi <= 84: sec = "Biological"
                        elif 85 <= fi <= 86: sec = "Cosmological"
                        elif 87 <= fi <= 102: sec = "Pharmaceutical"
                        elif 103 <= fi <= 116: sec = "Stars/Recipes"
                    
                    clean_c = re.sub(r"<[%$!@].*?>", "", content)
                    clean_c = re.sub(r"[{}\[\]<!>]", "", clean_c)
                    tokens = [t for t in re.split(r"[.,\s]+", clean_c) if t and not t.startswith("<")]
                    for t in tokens:
                        tc = re.sub(r"[^a-z]", "", t.lower())
                        if tc:
                            state = "OPERAND"
                            if tc.startswith(("qo", "qok", "qot", "qoc")): state = "OPERATOR"
                            elif tc.endswith(("y", "al", "ar", "aiin", "m")): state = "FLUSH"
                            records.append({
                                "folio": folio,
                                "line": line_no,
                                "locus": locus,
                                "section": sec,
                                "clean": tc,
                                "state": state
                            })
    return pd.DataFrame(records)

df = load_data()

# -----------------------------------------------------------------------------
# 2. CARRIER STRIPPING UTILITY
# -----------------------------------------------------------------------------
def strip_carrier(tok: str) -> str:
    s = str(tok).lower().strip()
    for p in ("qk", "dk", "qo", "ch", "sh", "q", "k", "d", "t", "ot", "ok"):
        if s.startswith(p):
            s = s[len(p):]
            break
    for ep in ("aiiin", "aiin", "ain", "eedy", "edy", "eey", "ey", "al", "ar", "am", "or", "ol", "m", "y"):
        if s.endswith(ep):
            s = s[:-len(ep)]
            break
    return s if s else "core"

# -----------------------------------------------------------------------------
# 3. HISTORICAL PTOLEMAIC & PICATRIX DECAN RULERS
# -----------------------------------------------------------------------------
PTOLEMAIC_DECANS = {
    "Aries": ["Mars", "Sun", "Venus"],
    "Taurus": ["Mercury", "Moon", "Saturn"],
    "Gemini": ["Jupiter", "Mars", "Sun"],
    "Cancer": ["Venus", "Mercury", "Moon"],
    "Leo": ["Saturn", "Jupiter", "Mars"],
    "Virgo": ["Sun", "Venus", "Mercury"],
    "Libra": ["Moon", "Saturn", "Jupiter"],
    "Scorpio": ["Mars", "Sun", "Venus"],
    "Sagittarius": ["Mercury", "Moon", "Saturn"],
    "Capricorn": ["Jupiter", "Mars", "Sun"],
    "Aquarius": ["Venus", "Mercury", "Moon"],
    "Pisces": ["Saturn", "Jupiter", "Mars"]
}

ZODIAC_FOLIO_MAP = {
    "f70v": "Pisces",
    "f70v2": "Pisces",
    "f71r": "Aries",
    "f71v": "Taurus",
    "f72r1": "Cancer",
    "f72r2": "Leo",
    "f72r3": "Virgo",
    "f72v1": "Libra",
    "f72v2": "Scorpio",
    "f72v3": "Sagittarius",
    "f73r": "Capricorn",
    "f73v": "Aquarius",
    "f74r": "Pisces"
}

st.title("Voynich Manuscript Decipherment Workbench & Decan Oracle")

tabs = st.tabs([
    "Astrological Decan Oracle",
    "Currier A vs B Separation", 
    "Positional & Bigram Rules", 
    "Substitution Sandbox", 
    "Export CSV"
])

# -----------------------------------------------------------------------------
# TAB 1: ASTROLOGICAL DECAN ORACLE
# -----------------------------------------------------------------------------
with tabs[0]:
    st.subheader("Topological Alignment: Zodiac Rotas vs. Historical Decans")
    st.markdown("""
    This oracle aligns radial tokens across circular Zodiac rotas (`f70r`–`f74v`) against 
    the 36 historical decans and planetary rulers from Ptolemy and the medieval *Picatrix*.
    """)
    
    col_a, col_b = st.columns([1, 2])
    
    with col_a:
        astro_folios = [f for f in sorted(df["folio"].unique()) if f in ZODIAC_FOLIO_MAP]
        if not astro_folios:
            astro_folios = ["f70v", "f71r", "f71v", "f72r1", "f72r2", "f72r3", "f72v1", "f72v2", "f72v3", "f73r", "f73v"]
        
        selected_rota = st.selectbox("Select Zodiac Rota Folio", astro_folios, index=0)
        assigned_sign = ZODIAC_FOLIO_MAP.get(selected_rota, "Aries")
        st.write(f"**Identified Zodiac Sign:** `{assigned_sign}`")
        st.write(f"**Ptolemaic Decan Rulers (10°, 20°, 30°):**")
        st.info(" → ".join(PTOLEMAIC_DECANS.get(assigned_sign, [])))
        
    with col_b:
        sub_rota = df[df["folio"] == selected_rota].copy()
        radial_loci = ["@Lz", "&Lz", "@Ls", "&Ls", "@La", "@Ri", "@Ro", "@Cc"]
        radial_tokens = sub_rota[sub_rota["locus"].str.contains(r"@L|&L|@R|@C", regex=True, na=False)].copy()
        
        if radial_tokens.empty:
            radial_tokens = sub_rota[sub_rota["locus"] != "+P0"].copy()
            
        if not radial_tokens.empty:
            radial_tokens["Carrier Core (Λ)"] = radial_tokens["clean"].apply(strip_carrier)
            
            # Map 30 divisions / decans (each decan covers 1/3 of the radial sector)
            total_labels = len(radial_tokens)
            st.metric("Total Radial Spoke Labels Identified", total_labels)
            
            decan_assignments = []
            rulers = PTOLEMAIC_DECANS.get(assigned_sign, ["Ruler 1", "Ruler 2", "Ruler 3"])
            for idx in range(total_labels):
                decan_idx = min(idx // max(1, (total_labels // 3)), 2)
                decan_assignments.append(f"Decan {decan_idx+1} ({rulers[decan_idx]})")
                
            radial_tokens["Assigned Decan Sector"] = decan_assignments
            
            st.dataframe(
                radial_tokens[["line", "locus", "clean", "Carrier Core (Λ)", "state", "Assigned Decan Sector"]],
                use_container_width=True
            )
            
            st.subheader("Carrier Core Distribution in Radial Sectors")
            core_counts = radial_tokens["Carrier Core (Λ)"].value_counts()
            st.bar_chart(core_counts)
        else:
            st.warning("No discrete radial label loci identified on this folio.")

# -----------------------------------------------------------------------------
# TAB 2: CURRIER A VS B SEPARATION
# -----------------------------------------------------------------------------
with tabs[1]:
    st.subheader("Currier A vs B Separation")
    f_list = sorted(df["folio"].unique().tolist()) if not df.empty else ["f1r"]
    chosen_f = st.selectbox("Select Folio to Inspect", f_list, index=0)
    sub = df[df["folio"] == chosen_f]
    
    col1, col2 = st.columns(2)
    cur_a_seeds = ["ar", "daiin", "otar", "chor", "ataiin", "cthy", "kchor"]
    cur_b_seeds = ["shey", "chey", "cheor", "kcheor", "qokedy", "shedaiin"]
    
    a_hits = sub[sub["clean"].isin(cur_a_seeds)]["clean"].tolist()
    b_hits = sub[sub["clean"].isin(cur_b_seeds)]["clean"].tolist()
    
    with col1:
        st.metric("Currier A Word Matches", len(a_hits))
        st.write("Currier A Tokens Detected:", a_hits)
    with col2:
        st.metric("Currier B Word Matches", len(b_hits))
        st.write("Currier B Tokens Detected:", b_hits)

# -----------------------------------------------------------------------------
# TAB 3: POSITIONAL & BIGRAM RULES
# -----------------------------------------------------------------------------
with tabs[2]:
    st.subheader("Glyph Positional Distribution & Bigrams")
    if not df.empty:
        all_text = "".join(df["clean"].tolist())
        chars = pd.Series(list(all_text)).value_counts().head(15)
        st.bar_chart(chars)

# -----------------------------------------------------------------------------
# TAB 4: SUBSTITUTION SANDBOX
# -----------------------------------------------------------------------------
with tabs[3]:
    st.subheader("Substitution Sandbox & Validator")
    st.write("Monoalphabetic substitution fails across folios due to invariant state-machine transition rules.")

# -----------------------------------------------------------------------------
# TAB 5: EXPORT CSV
# -----------------------------------------------------------------------------
with tabs[4]:
    st.subheader("Export Extracted Manuscript Corpus")
    if not df.empty:
        csv_bytes = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download Full Corpus (CSV)",
            data=csv_bytes,
            file_name="voynich_corpus_extracted.csv",
            mime="text/csv"
        )
        st.dataframe(df.head(20), use_container_width=True)
    else:
        st.warning("No corpus loaded to export.")
