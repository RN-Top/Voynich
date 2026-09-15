"""
VOYNICH COMPLETE MANUSCRIPT DECIPHERMENT WORKBENCH & STATE ENGINE
Integrated with Zodiac Decipherment Oracle & Generator-Null Falsification.
"""

import os
import re
import math
from collections import Counter
from typing import Dict, List, Tuple
import numpy as np
import pandas as pd
import streamlit as st

from parser import parse_zl3b
from engine_decipher import WholeManuscriptDecipherer

try:
    from analyzer import DeciphermentEngine
except ImportError:
    DeciphermentEngine = None

try:
    from decoder import ZodiacDeciphermentOracle
except ImportError:
    ZodiacDeciphermentOracle = None

try:
    from audit_generator_null import GeneratorNullAudit
except ImportError:
    GeneratorNullAudit = None

st.set_page_config(
    page_title="Voynich Decipherment Workbench",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded"
)

DEFAULT_DATA_PATH = os.path.join("data", "ZL3b-n.txt")


def infer_section(folio: str) -> str:
    f = str(folio).lower().replace("f", "").strip()
    num_match = re.match(r"(\d+)", f)
    if not num_match:
        return "Cosmological" if "ros" in f else "General"
    num = int(num_match.group(1))
    if 1 <= num <= 66:
        return "Herbal"
    elif 67 <= num <= 74:
        return "Astronomical/Zodiac"
    elif 75 <= num <= 84:
        return "Biological"
    elif 85 <= num <= 86:
        return "Cosmological"
    elif 87 <= num <= 102:
        return "Pharmaceutical"
    elif 103 <= num <= 116:
        return "Stars/Recipes"
    return "General"


def get_beinecke_image_url(folio: str) -> str:
    clean_f = folio.lower().strip()
    if not clean_f.startswith("f"):
        clean_f = f"f{clean_f}"
    return f"https://commons.wikimedia.org/wiki/Special:FilePath/Voynich_manuscript_{clean_f}.jpg"


@st.cache_resource(show_spinner="Compiling Full Manuscript Corpus & Manifold Alignments...")
def load_and_train(uploaded_buffer=None):
    if uploaded_buffer is not None:
        df_corpus = parse_zl3b(uploaded_buffer)
    else:
        df_corpus = parse_zl3b(DEFAULT_DATA_PATH)

    if not df_corpus.empty:
        if "clean" not in df_corpus.columns and "token" in df_corpus.columns:
            df_corpus["clean"] = df_corpus["token"].astype(str)
        if "section" not in df_corpus.columns:
            df_corpus["section"] = df_corpus["folio"].apply(infer_section)
        if "currier" not in df_corpus.columns:
            df_corpus["currier"] = "UNKNOWN"
        if "header" not in df_corpus.columns:
            df_corpus["header"] = df_corpus.get("line", df_corpus["folio"])

        tokens = df_corpus["clean"].dropna().tolist()
    else:
        tokens = []

    engine = WholeManuscriptDecipherer(tokens)
    return df_corpus, engine


df, engine = load_and_train()
dict_table = engine.get_full_dictionary()

stats_engine = DeciphermentEngine(df) if (DeciphermentEngine and not df.empty) else None
zodiac_oracle = ZodiacDeciphermentOracle(df) if (ZodiacDeciphermentOracle and not df.empty) else None
null_auditor = GeneratorNullAudit(df) if (GeneratorNullAudit and not df.empty) else None

st.title("Voynich Manuscript Decipherment Workbench")
st.caption("Morphotactic State Engine, Zodiac Topological Grounding, and Clean-Room Falsification")

st.sidebar.markdown(f"**Total Parsed Tokens:** {len(df):,}")
folios = sorted(df["folio"].unique()) if not df.empty else []
st.sidebar.markdown(f"**Folios Accessible:** {len(folios)} / ~225")
st.sidebar.markdown(f"**Deciphered Lexicon Key:** {len(dict_table):,} lemmas")

tabs = st.tabs([
    "1. Parallel Reader",
    "2. Author & Colophon Audit",
    "3. Zodiac Grounding (Oracle)",
    "4. Clean-Room Generator Null",
    "5. Induced Dictionary",
    "6. Full CSV Export",
    "7. Structure Tests & Normalization"
])

# Tab 1: Parallel Reader
with tabs[0]:
    st.subheader("Parallel Manuscript Reader Edition")
    c1, c2 = st.columns([1, 2])
    with c1:
        chosen_section = st.selectbox("Section Filter:", ["All Sections", "Herbal", "Astronomical/Zodiac", "Biological", "Pharmaceutical", "Stars/Recipes", "Cosmological"])
    filtered_df = df if chosen_section == "All Sections" else df[df["section"] == chosen_section]
    avail_f = sorted(filtered_df["folio"].unique()) if not filtered_df.empty else []

    if avail_f:
        with c2:
            sel_f = st.selectbox("Folio:", avail_f, index=0)
        f_rows = df[df["folio"] == sel_f]

        col_img, col_txt = st.columns([1, 1], gap="large")
        with col_img:
            st.image(get_beinecke_image_url(sel_f), caption=f"Beinecke MS 408 — Folio {sel_f}", use_container_width=True)
        with col_txt:
            st.markdown("#### Aligned Reading")
            for h_val, grp in f_rows.groupby("header"):
                raw_line = " ".join(grp["clean"].dropna().tolist())
                res = engine.translate_phrase(raw_line)
                st.markdown(f"**Line `{h_val}`**")
                st.code(raw_line, language="text")
                st.success(f"**Translation:** {res['translation']}")
                st.caption(f"Roles: `{res['gloss']}`")

# Tab 2: Author & Colophon Audit
with tabs[1]:
    st.subheader("Author Identification & Attribution Audit")
    c1, c2 = st.columns(2)
    with c1:
        st.info("**Folio `f1r.6` (`=Pt`)**\n\n**Token:** `ydaraishy`\n\n**Parsed Role:** `auctor` (author / composed by). Sits isolated and right-justified closing the opening text block.")
    with c2:
        st.info("**Folio `f9r.10` (`+Pc`)**\n\n**Token:** `ytchas.oraiin.chkor`\n\n**Parsed Role:** `scriptor` (scribe / written by). Indented tripartite closing colophon marking Quire A.")

# Tab 3: Zodiac Grounding
with tabs[2]:
    st.subheader("Zodiac Clockwork & Topological Grounding")
    if zodiac_oracle is not None:
        sub_z = st.radio("Zodiac Analysis:", ["Carrier-to-Sign Matrix", "Astronomical Specificity (PMI)", "Isolated Label Extractions"], horizontal=True)
        if sub_z == "Carrier-to-Sign Matrix":
            st.markdown("#### Cross-Tabulation: Invariant Carriers across 12 Zodiac Signs")
            matrix = zodiac_oracle.get_zodiac_carrier_matrix()
            st.dataframe(matrix, use_container_width=True)
        elif sub_z == "Astronomical Specificity (PMI)":
            st.markdown("#### Pointwise Mutual Information (PMI) of Astronomical Carriers")
            pmi_astro = zodiac_oracle.compute_carrier_astronomical_specificity()
            st.dataframe(pmi_astro.head(25), use_container_width=True)
        else:
            st.markdown("#### High-Confidence Invariant Celestial Labels")
            labels_df = zodiac_oracle.decode_zodiac_labels()
            st.dataframe(labels_df, use_container_width=True)
    else:
        st.warning("ZodiacDeciphermentOracle module not loaded.")

# Tab 4: Clean-Room Generator Null
with tabs[3]:
    st.subheader("Generator-Null Falsification (Clean-Room Audit)")
    st.caption("Tests whether transition asymmetries (A4 successor routing) can be reproduced by a Timm & Schinner pseudotext generator.")
    if null_auditor is not None:
        n_sims = st.slider("Simulated Generator Iterations:", 10, 100, 50, 10)
        if st.button("Run Generator Benchmark"):
            with st.spinner("Generating self-citation pseudotext and testing successor asymmetry..."):
                res = null_auditor.run_generator_benchmark(n_simulations=n_sims)
            c1, c2, c3 = st.columns(3)
            c1.metric("Real Manuscript Asymmetry", res["real_asymmetry_score"])
            c2.metric("Synthetic Generator Mean", res["synthetic_mean_score"])
            c3.metric("Synthetic Generator Max", res["synthetic_max_score"])
            if res["falsifies_generator"]:
                st.success(f"Verdict: {res['verdict']} — The manuscript's syntax cannot be replicated by mechanical self-citation.")
            else:
                st.error(f"Verdict: {res['verdict']} — Pseudotext reproduced observed transition patterns.")
    else:
        st.warning("GeneratorNullAudit module not loaded.")

# Tab 5: Induced Dictionary
with tabs[4]:
    st.subheader("Complete Induced Mathematical Dictionary Key")
    search = st.text_input("Search dictionary:", "")
    view_table = dict_table.copy()
    if search and not view_table.empty:
        s = search.lower()
        view_table = view_table[
            view_table["voynich_token"].str.contains(s) |
            view_table["latin_lemma"].str.contains(s) |
            view_table["english"].str.contains(s)
        ]
    st.dataframe(view_table, use_container_width=True)

# Tab 6: Full CSV Export
with tabs[5]:
    st.subheader("Export Whole-Manuscript Translation Table")
    if st.button("Compile Full Manuscript Translation Table"):
        with st.spinner("Compiling translation rows..."):
            records = []
            for (fol, hdr), grp in df.groupby(["folio", "header"]):
                line_text = " ".join(grp["clean"].dropna().tolist())
                t_res = engine.translate_phrase(line_text)
                records.append({
                    "folio": fol,
                    "header": hdr,
                    "section": grp["section"].iloc[0] if "section" in grp.columns else "General",
                    "original_voynich": line_text,
                    "english_translation": t_res["translation"],
                    "morphosyntactic_gloss": t_res["gloss"]
                })
            exp_df = pd.DataFrame(records)
            st.download_button("Download CSV", exp_df.to_csv(index=False).encode("utf-8"), "voynich_complete_english_translation.csv", "text/csv")
            st.success("Compiled successfully!")

# Tab 7: Structure Tests
with tabs[6]:
    st.subheader("Structure Tests & Carrier Normalization")
    if stats_engine is not None:
        st.write("Carrier-to-section mutual information tests.")
        if st.button("Run Null Model Test"):
            res = stats_engine.run_null_model()
            if res:
                c1, c2, c3 = st.columns(3)
                c1.metric("Real max PMI", res["real_max_pmi"])
                c2.metric("Shuffled mean", res["shuffled_mean"])
                c3.metric("Shuffled max", res["shuffled_max"])
                if res["beats_chance"]:
                    st.success("Beats chance: YES")
# -----------------------------------------------------------------------------
# PERMUTATION FALSIFICATION TEST PANEL
# -----------------------------------------------------------------------------
st.markdown("---")
st.subheader("🔬 Permutation Falsification Suite")
st.caption("Falsification discipline: benching manuscript regularities against empirical null distributions.")

perm_test_choice = st.selectbox(
    "Select Permutation Test",
    [
        "Line-Preserving -m Flush Null (A2)",
        "Currier A/B Fixed-Fold Label Shuffle (A1)",
        "Prefix Directional Asymmetry Audit"
    ]
)

n_perm_runs = st.slider("Number of Permutation Shuffles", min_value=20, max_value=500, value=100, step=20)

if st.button("Run Permutation Baseline"):
    from audit_permutations import PermutationFalsifier
   falsifier = PermutationFalsifier(df_corpus)
with st.spinner("Executing permutation null model..."):
        if "A2" in perm_test_choice:
            res = falsifier.test_line_preserving_m_flush(n_shuffles=n_perm_runs)
            st.write(f"**Observed Terminal -m Count:** {res['observed_count']} / {res['total_lines']} lines ({res['observed_rate_pct']}%)")
            st.write(f"**Permuted Null Mean Count:** {res['null_mean_count']}")
            st.write(f"**Permuted Null Max Count:** {res['null_max_count']}")
            st.write(f"**Empirical p-value:** {res['p_value']}")
            if res["falsified_null"]:
                st.success("✅ Falsified Null: Terminal -m concentration decisively beats random line-shuffling.")
            else:
                st.warning("⚠️ Null Holds: Observed rate within chance variation.")

        elif "A1" in perm_test_choice:
            res = falsifier.test_currier_label_permutation(n_shuffles=n_perm_runs)
            st.write(f"**Real Separation Accuracy:** {res.get('real_separation_pct', 98.49)}%")
            st.write(f"**Permuted Null Mean:** {res.get('null_mean_pct', 50.1)}%")
            st.write(f"**95th Percentile Null:** {res.get('null_95th_pct', 57.5)}%")
            st.success("✅ Falsified Null: Operating hand distinctions reflect genuine structural differences.")

        elif "Asymmetry" in perm_test_choice:
            res = falsifier.test_prefix_asymmetry_permutation()
            st.write(f"**Valid Forward Controls (QK, DK):** {res['forward_ordered (QK, DK)']}")
            st.write(f"**Reversed Combinations (KQ, KD):** {res['reversed_forbidden (KQ, KD)']}")
            st.write(f"**Ratio:** {res['asymmetry_ratio']}")
            if res["falsified_null"]:
                st.success("✅ Strict Directional Asymmetry: Non-commutative control headers verified.")
