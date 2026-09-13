"""
VOYNICH COMPLETE MANUSCRIPT DECIPHERMENT WORKBENCH & PARALLEL READER
- Parallel Facsimile Reader (Beinecke digital scan beside decoded English & raw files)
- Dedicated Author Identification & Colophon Audit Inspector
- Live Sequence Translator & Induced Lexical Dictionary
- Whole-Manuscript CSV Export
- Executive Findings & 600-Year Decipherment Verdict
- Null model / holdout structure tests
"""

import os
import re
import pandas as pd
import streamlit as st

from parser import parse_zl3b
from engine_decipher import WholeManuscriptDecipherer
from analyzer import DeciphermentEngine

st.set_page_config(
    page_title="Voynich Manuscript Complete Decipherment Workbench",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded"
)

DEFAULT_DATA_PATH = os.path.join("data", "ZL3b-n.txt")


def infer_section(folio: str) -> str:
    """Infers thematic section if missing from parser DataFrame."""
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
    """Generates standard digital facsimile URLs for Beinecke MS 408 folios via Wikimedia Commons."""
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


def extract_author_audit(filepath: str = DEFAULT_DATA_PATH):
    marginal_findings = []
    structural_colophons = []

    if not os.path.exists(filepath):
        return marginal_findings, pd.DataFrame(structural_colophons)

    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()

    current_folio = "f1r"
    token_regex = re.compile(r"<f(\d+[rv]\d*)\.(\d+),([@=+*][A-Za-z0-9_]+)>\s*(.*)")

    for line in lines:
        line_str = line.strip()
        f_match = re.match(r"<