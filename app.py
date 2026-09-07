import streamlit as st
import pandas as pd
from parser import parse_zl3b, ensure_full_corpus, CORPUS_PATH
from engine_decipher import LatentGrammarInducer, WholeManuscriptDecipherer

st.set_page_config(page_title="Voynich Decipherment Workbench", layout="wide")

@st.cache_data(show_spinner="Ingesting full manuscript (~38,000 tokens)...")
def load_and_decipher():
    ensure_full_corpus()
    df = parse_zl3b(CORPUS_PATH)
    all_tokens = df["clean"].tolist()
    decipherer = WholeManuscriptDecipherer(all_tokens)
    return df, decipherer

st.title("Voynich Manuscript: Full Computational Decipherment & Reader")

df, decipherer = load_and_decipher()
folios = sorted(list(df["folio"].unique()))

tab1, tab2, tab3 = st.tabs(["Manuscript Reader", "Full Lexicon Key", "Interactive Translator"])

with tab1:
    st.subheader("Browse Folios (f1r to f116v)")
    selected_folio = st.selectbox("Select Folio:", folios)
    folio_df = df[df["folio"] == selected_folio]
    
    st.write(f"Total lines: {folio_df['header'].nunique()} | Currier Mode: {folio_df['currier'].iloc[0]}")
    
    for header, group in folio_df.groupby("header", sort=False):
        raw_line = " ".join(group["clean"])
        res = decipherer.translate_phrase(raw_line)
        with st.expander(f"Line: {header}", expanded=True):
            st.markdown(f"**Voynich:** `{raw_line}`")
            st.markdown(f"**Grammar Gloss:** {res['gloss']}")
            st.markdown(f"**Decoded Text:** {res['translation']}")

with tab2:
    st.subheader("Derived Lexicon & Alignment Key")
    dict_df = decipherer.get_full_dictionary()
    st.dataframe(dict_df, use_container_width=True)

with tab3:
    st.subheader("Custom Phrase Translator")
    user_input = st.text_input("Enter Voynich tokens separated by spaces:", value="fachys ykal ar ataiin shol")
    if user_input:
        out = decipherer.translate_phrase(user_input)
        st.write("**Gloss:**", out["gloss"])
        st.write("**Output:**", out["translation"])
