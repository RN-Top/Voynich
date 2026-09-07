"""
VOYNICH MATHEMATICAL DECIPHERMENT WORKBENCH
Interactive Streamlit application displaying the induced grammar key,
derived mathematical dictionary, and full English translation pipeline.
"""

import os
import pandas as pd
import streamlit as st

from parser import parse_zl3b
from engine_decipher import FullDeciphermentPipeline

st.set_page_config(
    page_title="Voynich Decipherment & Translation Workbench",
    page_icon="📜",
    layout="wide",
    initial_sidebar_state="expanded"
)

DEFAULT_DATA_PATH = os.path.join("data", "ZL3b-n.txt")


@st.cache_resource(show_spinner="Running SVD Grammar Induction & Procrustes Lexicon Alignment...")
def initialize_models(filepath: str):
    df_corpus = parse_zl3b(filepath)
    tokens = df_corpus["clean"].dropna().tolist()
    pipeline = FullDeciphermentPipeline(tokens)
    return df_corpus, pipeline


st.title("Voynich Mathematical Decipherment Workbench")
st.caption("Unsupervised Grammar Induction, PPMI Semantic Alignment, and Automated English Translation")

if not os.path.exists(DEFAULT_DATA_PATH):
    st.error(f"Transliteration corpus not found at `{DEFAULT_DATA_PATH}`. Please place `ZL3b-n.txt` in the `data/` folder.")
    st.stop()

df, pipeline = initialize_models(DEFAULT_DATA_PATH)
dict_df = pipeline.get_dictionary_table()

# Sidebar Statistics
st.sidebar.markdown("### Corpus Statistics")
st.sidebar.markdown(f"**Total Tokens:** {len(df):,}")
st.sidebar.markdown(f"**Unique Vocabulary:** {len(dict_df):,} entries")
st.sidebar.markdown(f"**Grammar Classes:** 4 Latent Roles")

tabs = st.tabs([
    "1. Live English Translator",
    "2. Derived Dictionary Key",
    "3. Induced Grammar Key",
    "4. Full Folio Reader Edition"
])

# =============================================================================
# TAB 1: Live English Translator
# =============================================================================
with tabs[0]:
    st.subheader("Interactive Translation Console")
    st.markdown(
        "Enter any raw Voynich transliteration string to see its mathematically induced syntactic roles "
        "and corresponding English translation."
    )

    preset_phrases = [
        "qokedy qokeey daiin okedy qokal chdam",
        "fachys ykal ar ataiin shol shory",
        "otcheody qokedy daiin chedain shedy",
        "pshol chor otshal chopy cphol chody"
    ]
    selected_preset = st.selectbox("Sample Transliteration Lines:", preset_phrases)
    user_line = st.text_input("Or enter custom Voynich token string:", selected_preset)

    if user_line:
        output = pipeline.translate_sequence(user_line)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### Morphosyntactic Gloss")
            st.info(output["gloss"])
            st.caption("[OPE] = Operand Noun | [OPE] = Operator Verb | [MOD] = Modifier Adj | [TER] = Terminal Flush")

        with col2:
            st.markdown("#### Synthesized English Reading")
            st.success(f"### {output['translation']}")
            st.caption("Constructed from the mathematically aligned 15th-century Latin lemma matrix.")

# =============================================================================
# TAB 2: Derived Dictionary Key
# =============================================================================
with tabs[1]:
    st.subheader("Derived Lexical Dictionary Key")
    st.markdown(
        "Lexicon constructed by computing Positive Pointwise Mutual Information (PPMI) vectors "
        "and aligning them to 15th-century medical/herbal control spaces."
    )
    search = st.text_input("Filter Dictionary by Voynich Token or English Word:", "")
    view_table = dict_df.copy()
    if search:
        view_table = view_table[
            view_table["voynich_token"].str.contains(search.lower()) |
            view_table["english"].str.contains(search.lower())
        ]
    st.dataframe(view_table, use_container_width=True)

# =============================================================================
# TAB 3: Induced Grammar Key
# =============================================================================
with tabs[2]:
    st.subheader("Induced Syntactic Key")
    st.markdown(
        "Latent grammatical parts of speech induced directly from the Singular Value Decomposition (SVD) "
        "of empirical bigram transition probabilities."
    )

    col1, col2 = st.columns([1, 1.2])
    with col1:
        st.write("#### Lexicon Distribution Across Syntactic Roles")
        if not dict_df.empty:
            st.bar_chart(dict_df["induced_role"].value_counts())

    with col2:
        st.write("#### Grammatical Role Definitions")
        st.markdown("""
        * **`OPERAND_NOUN`**: Conserved lexical stems representing objects, plant parts, vessels, and celestial entities[span_11](start_span)[span_11](end_span).
        * **`OPERATOR_VERB`**: Iterative compute and transformation routines (e.g. heating, boiling, mixing, extracting)[span_12](start_span)[span_12](end_span)[span_13](start_span)[span_13](end_span).
        * **`MODIFIER_ADJ`**: Stative tuning registers indicating condition, quality, or dosage degree[span_14](start_span)[span_14](end_span).
        * **`TERMINAL_FLUSH`**: Rigid line-boundary execution flushes (verified by the line-final `-m` behavior)[span_15](start_span)[span_15](end_span)[span_16](start_span)[span_16](end_span).
        """)

# =============================================================================
# TAB 4: Full Folio Reader Edition
# =============================================================================
with tabs[3]:
    st.subheader("Manuscript Parallel Reader Edition")
    folios = sorted(df["folio"].unique())
    chosen_folio = st.selectbox("Select Folio to Translate:", folios, index=0)
    folio_data = df[df["folio"] == chosen_folio]

    st.markdown(f"**Folio:** `{chosen_folio}` | **Currier Language Hand:** `{folio_data['currier'].iloc[0]}`")
    st.markdown("---")

    for header, group in folio_data.groupby("header"):
        line_raw = " ".join(group["clean"].tolist())
        res = pipeline.translate_sequence(line_raw)
        st.markdown(f"**Line `{header}`**")
        st.code(line_raw, language="text")
        st.markdown(f"**English Translation:** *{res['translation']}*")
        st.caption(f"Gloss: `{res['gloss']}`")
        st.markdown("---")
