import streamlit as st
import pandas as pd
import numpy as np
import os
import re
import urllib.request

st.set_page_config(page_title="Voynich Decipherment Workbench", layout="wide")

@st.cache_data(show_spinner="Loading manuscript corpus...")
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

st.title("Voynich Manuscript Analysis & Export Workbench")

tabs = st.tabs([
    "Currier A vs B Separation", 
    "Positional & Bigram Rules", 
    "Substitution Sandbox", 
    "Export CSV"
])

# TAB 1: CURRIER SEPARATION
with tabs[0]:
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

# TAB 2: POSITIONAL & BIGRAM RULES
with tabs[1]:
    st.subheader("Glyph Positional Distribution & Bigrams")
    if not df.empty:
        all_text = "".join(df["clean"].tolist())
        chars = pd.Series(list(all_text)).value_counts().head(15)
        st.bar_chart(chars)

# TAB 3: SUBSTITUTION SANDBOX
with tabs[2]:
    st.subheader("Substitution Sandbox & Validator")
    st.write("Simple monoalphabetic substitution fails to produce coherent language across both scribal hands.")

# TAB 4: EXPORT CSV
with tabs[3]:
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
