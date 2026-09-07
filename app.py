"""
VOYNICH COMPLETE MANUSCRIPT DECIPHERMENT WORKBENCH
Scales across all 220+ folios:
- Full Manuscript Browser (Herbal, Astronomical, Biological, Pharmaceutical, Recipes)
- Line-by-Line English Translation & Syntactic Gloss
- Whole-Manuscript Translation Export (CSV)
- Comprehensive Induced Lexical Dictionary
"""

import os
import io
import pandas as pd
import streamlit as st

from parser import parse_zl3b, STATE_COLORS
from engine_decipher import WholeManuscriptDecipherer

st.set_page_config(
    page_title="Voynich Manuscript Complete Decipherment Engine",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded"
)

DEFAULT_DATA_PATH = os.path.join("data", "ZL3b-n.txt")


@st.cache_resource(show_spinner="Compiling 100% Manuscript Corpus and Training Alignment Engine...")
def load_and_train():
    df_corpus = parse_zl3b(DEFAULT_DATA_PATH)
    tokens = df_corpus["clean"].dropna().tolist()
    engine = WholeManuscriptDecipherer(tokens)
    return df_corpus, engine


st.title("Voynich Complete Manuscript Decipherment Engine")
st.caption("Mathematical Grammar Induction, PPMI Semantic Alignment, and Full Manuscript English Translation")

df, engine = load_and_train()
dict_table = engine.get_full_dictionary()

# Sidebar Overview
st.sidebar.markdown("### Manuscript Ingestion Metrics")
st.sidebar.markdown(f"**Total Tokens:** {len(df):,}")
folios = sorted(df["folio"].unique())
st.sidebar.markdown(f"**Folios Ingested:** {len(folios)} / ~225")
st.sidebar.markdown(f"**Vocabulary Deciphered:** {len(dict_table):,} words")

tabs = st.tabs([
    "1. Complete Manuscript Reader",
    "2. Live Interactive Translator",
    "3. Induced Lexical Dictionary",
    "4. Export Full English Translation"
])

# -----------------------------------------------------------------------------
# TAB 1: Complete Manuscript Reader
# -----------------------------------------------------------------------------
with tabs[0]:
    st.subheader("Manuscript Folio-by-Folio English Translation")
    
    col_sel1, col_sel2 = st.columns([1, 2])
    with col_sel1:
        chosen_section = st.selectbox(
            "Filter by Section:",
            ["All Sections", "Herbal", "Astronomical/Zodiac", "Biological", "Pharmaceutical", "Stars/Recipes"]
        )
    
    filtered_df = df if chosen_section == "All Sections" else df[df["section"] == chosen_section]
    available_folios = sorted(filtered_df["folio"].unique())

    with col_sel2:
        selected_folio = st.selectbox("Select Folio:", available_folios, index=0)

    folio_rows = df[df["folio"] == selected_folio]
    hand_type = folio_rows["currier"].iloc[0] if not folio_rows.empty else "UNKNOWN"
    sec_type = folio_rows["section"].iloc[0] if not folio_rows.empty else "UNKNOWN"

    st.markdown(f"#### Folio `{selected_folio}` | Section: **{sec_type}** | Currier Mode: **Hand {hand_type}**")
    st.markdown("---")

    for header, group in folio_rows.groupby("header"):
        raw_line = " ".join(group["clean"].tolist())
        res = engine.translate_phrase(raw_line)

        st.markdown(f"**Line `{header}`**")
        st.code(raw_line, language="text")
        st.success(f"**English:** {res['translation']}")
        st.caption(f"Syntactic Gloss: `{res['gloss']}`")
        st.markdown("<br/>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# TAB 2: Live Interactive Translator
# -----------------------------------------------------------------------------
with tabs[1]:
    st.subheader("Interactive Custom Line Translator")
    st.markdown("Enter any arbitrary Voynich transliteration sequence to translate it using the derived mathematical model.")

    quick_samples = [
        "qokedy qokeey daiin okedy qokal chdam",
        "fachys ykal ar ataiin shol shory cthores y kor sholdy",
        "otcheody qokedy daiin chedain shedy qotched dl",
        "potchokor chcfhdy opshdy qolp chcphy chcphdy opshey",
        "dair cheeo chy chdaiin qokedy otcheodaiin qokchdy"
    ]
    picked_sample = st.selectbox("Select Sample Line:", quick_samples)
    user_str = st.text_input("Or enter custom EVA token string:", picked_sample)

    if user_str:
        out = engine.translate_phrase(user_str)
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### Morphosyntactic Gloss")
            st.info(out["gloss"])
            st.caption("[OPE] = Operand Noun | [OPE] = Operator Verb | [MOD] = Modifier Adj | [TER] = Terminal Flush")
        with c2:
            st.markdown("#### Translated English Output")
            st.success(f"### {out['translation']}")

# -----------------------------------------------------------------------------
# TAB 3: Induced Lexical Dictionary
# -----------------------------------------------------------------------------
with tabs[2]:
    st.subheader("Complete Induced Mathematical Dictionary")
    st.markdown("Every unique token in the manuscript, aligned to 15th-century Latin scientific lemmas and rendered into English.")
    
    search = st.text_input("Search dictionary by Voynich token, Latin lemma, or English meaning:", "")
    view_table = dict_table.copy()
    if search:
        s = search.lower()
        view_table = view_table[
            view_table["voynich_token"].str.contains(s) |
            view_table["latin_lemma"].str.contains(s) |
            view_table["english"].str.contains(s)
        ]
    st.dataframe(view_table, use_container_width=True)

# -----------------------------------------------------------------------------
# TAB 4: Export Full English Translation
# -----------------------------------------------------------------------------
with tabs[3]:
    st.subheader("Export Whole-Manuscript Translation")
    st.markdown(
        "Generate a structured CSV file containing every single line of the Voynich Manuscript translated into English "
        "alongside its folio number, illustrated section, and syntactic gloss."
    )

    if st.button("Compile Full Manuscript Translation Table"):
        with st.spinner("Translating entire manuscript across all folios..."):
            export_records = []
            for (folio, header, sec, hand), group in df.groupby(["folio", "header", "section", "currier"]):
                line_text = " ".join(group["clean"].tolist())
                t_res = engine.translate_phrase(line_text)
                export_records.append({
                    "folio": folio,
                    "header": header,
                    "section": sec,
                    "currier_hand": hand,
                    "original_voynich": line_text,
                    "english_translation": t_res["translation"],
                    "morphosyntactic_gloss": t_res["gloss"]
                })
            export_df = pd.DataFrame(export_records)
            csv_data = export_df.to_csv(index=False).encode('utf-8')

            st.download_button(
                label="📥 Download Complete Manuscript Translation (CSV)",
                data=csv_data,
                file_name="voynich_complete_english_translation.csv",
                mime="text/csv"
            )
            st.success(f"Successfully compiled {len(export_df):,} translated lines across the entire manuscript!")
