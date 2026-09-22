"""
tkTk
"""
import os
import re
from collections import Counter
import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title=" Voynich Workbench ",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 1. HISTORICAL LEXICON & SKELETON ---
CORE_LEXICON = [
    {"voynich_token": "ydaraishy", "stem": "ydaraishy", "latin_lemma": "auctor", "english": "author", "role": "OPERAND_NOUN"},
    {"voynich_token": "ytchas", "stem": "ytchas", "latin_lemma": "scriptor", "english": "scribe", "role": "OPERAND_NOUN"},
    {"voynich_token": "daiin", "stem": "daiin", "latin_lemma": "aqua", "english": "water", "role": "OPERAND_NOUN"},
    {"voynich_token": "chedy", "stem": "chedy", "latin_lemma": "herba", "english": "herb", "role": "OPERAND_NOUN"},
    {"voynich_token": "qokedy", "stem": "k", "latin_lemma": "coque", "english": "heat", "role": "OPERATOR_VERB"},
    {"voynich_token": "qokeey", "stem": "k", "latin_lemma": "misce", "english": "mix", "role": "OPERATOR_VERB"},
    {"voynich_token": "otcheod", "stem": "cheod", "latin_lemma": "stella", "english": "star", "role": "OPERAND_NOUN"},
    {"voynich_token": "oror", "stem": "oror", "latin_lemma": "finis", "english": "terminal marker", "role": "TERMINAL_FLUSH"},
]
dict_df = pd.DataFrame(CORE_LEXICON)

# --- 2. EMBEDDED CORPUS & TRANSLATOR ---
FALLBACK_CORPUS = [
    {"folio": "f1r", "line": "f1r.1", "clean": "fachys ykal ar ataiin shol"},
    {"folio": "f70v", "line": "f70v.1", "clean": "otcheod al opair al oteod air"},
    {"folio": "f103r", "line": "f103r.1", "clean": "daiin chedy qokedy chdam"},
    {"folio": "f114v", "line": "f114v.21", "clean": "otcheodaiin qopairam otcheody"},
    {"folio": "f116v", "line": "f116v.1", "clean": "oror sheey"},
]
df_corpus = pd.DataFrame(FALLBACK_CORPUS)

def translate_phrase(text):
    return text, f"[tk_translate: {text}]"

# --- 3. STREAMLIT UI ---
st.title(" Voynich Workbench (tkTk)")
st.caption("Simplified interface testing data integrity and layout.")

t_cribs, t_reader, t_lex = st.tabs([
    " Crib Alignment",
    " Manuscript Reader",
    " Lexicon Key",
])

with t_cribs:
    st.subheader("tkTk: Crib Alignment Matrix")
    st.info("tkTk placeholder for skeletal CV match data.")
    cribs_data = [
        {"Sign": "Pisces (f70v)", "Decan": "PASIS", "Match": "90% (tkTk)"},
        {"Sign": "Aries (f71r)", "Decan": "MARS", "Match": "85% (tkTk)"},
    ]
    st.dataframe(pd.DataFrame(cribs_data), use_container_width=True)

with t_reader:
    st.subheader("tkTk: Folio Reader")
    folios = sorted(df_corpus["folio"].unique())
    sel_f = st.selectbox("Select Folio", folios)
    for _, row in df_corpus[df_corpus["folio"] == sel_f].iterrows():
        with st.expander(f"Line {row['line']}", expanded=True):
            st.markdown(f"**Voynich:** `{row['clean']}`")
            st.caption(f"tk_translation placeholder.")

with t_lex:
    st.subheader("tkTk: Lexicon Key")
    st.dataframe(dict_df, use_container_width=True)
