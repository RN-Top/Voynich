import streamlit as st
import pandas as pd
import numpy as np
import re
from collections import Counter
import random

st.set_page_config(page_title="Voynich Decipherment Workbench", layout="wide")

st.title("Voynich Decipherment Workbench")
st.caption("Morphological Analysis, Syntactic Evaluation & Optimized Tournaments")

# ---------------------------------------------------------
# Sidebar: Data Source & Config
# ---------------------------------------------------------
st.sidebar.header("Data & Configuration")
uploaded_file = st.sidebar.file_uploader("Upload ZL3b Transcription / Text File", type=["txt", "csv", "csv"])

@st.cache_data
def load_and_clean_data(file):
    if file is None:
        # Fallback sample data generator
        sample_lines = [
            "fachys ykal ar ataiin shol shory cthesos chey keo dal chedy qokedy",
            "otaiin cthy shey dain qokaiin or chey cthey qotedy ol shedy chol",
            "daiin chedy ctheor otaiin chey shedy ctedy chekeor chedy",
            "qokeedy qokaiin sol cheol daiin ctheo qokedy cthee dal shey",
            "shedy qokain or cheor chedy dar shey daiin ctheor dal",
            "fachys ykey otaiin chey keor qokedy chedy qotedy ol chey",
            "otaiin shey qokaiin cthey cthes cheor keol chedy qotedy",
            "qotedy chedy otaiin daiin chey ctheo qokedy cheor shedy dal",
            "ykal ar chey keo cthesos qokaiin daiin shedy qotedy ol",
            "qokedy shedy chol otaiin ctheor chey daiin qokeedy chedy"
        ]
        parsed = []
        for idx, line in enumerate(sample_lines):
            tokens = line.split()
            for pos, tok in enumerate(tokens):
                parsed.append({
                    "folio": f"sample_f{idx//2 + 1}r",
                    "currier": "A" if (idx % 4 < 2) else "B",
                    "line": idx + 1,
                    "position": pos + 1,
                    "word": tok
                })
        return pd.DataFrame(parsed)

    try:
        if file.name.endswith(".csv"):
            df = pd.read_csv(file)
        else:
            raw_text = file.getvalue().decode("utf-8", errors="ignore")
            lines = [l.strip() for l in raw_text.splitlines() if l.strip() and not l.startswith(("#", "<"))]
            parsed = []
            for idx, line in enumerate(lines):
                tokens = re.findall(r"[a-z0-9*]+", line.lower())
                for pos, tok in enumerate(tokens):
                    parsed.append({
                        "folio": f"line_{idx+1}",
                        "currier": "A" if idx % 2 == 0 else "B",
                        "line": idx + 1,
                        "position": pos + 1,
                        "word": tok
                    })
            df = pd.DataFrame(parsed)
        st.sidebar.success("Custom data loaded successfully.")
        return df
    except Exception as e:
        st.sidebar.error(f"Error parsing file: {e}")
        st.stop()

df = load_and_clean_data(uploaded_file)

# Ensure required columns
required_cols = {"folio", "currier", "word"}
if not required_cols.issubset(df.columns):
    st.error(f"Data must contain at least columns: {required_cols}")
    st.stop()

# ---------------------------------------------------------
# Helper Functions: Morphological Parsing & Transition Scores
# ---------------------------------------------------------
PREFIXES = ("qo", "ch", "sh", "da", "ot", "cth", "y", "sa")
SUFFIXES = ("edy", "aiin", "iin", "ey", "ol", "or", "ar", "al", "y")

st.cache_data
def parse_affixes(word):
    """Splits an EVA word into Prefix, Core, Suffix."""
    w = str(word).lower()
    prefix = ""
    suffix = ""
    for p in sorted(PREFIXES, key=len, reverse=True):
        if w.startswith(p) and len(w) > len(p):
            prefix = p
            w = w[len(p):]
            break
    for s in sorted(SUFFIXES, key=len, reverse=True):
        if w.endswith(s) and len(w) > len(s):
            suffix = s
            w = w[:-len(s)]
            break
    core = w if w else "_"
    return prefix or "none", core, suffix or "none"

df["prefix"], df["core"], df["suffix"] = zip(*df["word"].apply(parse_affixes))
df["affix_role"] = df["prefix"] + "+" + df["suffix"]

def compute_bigram_mutual_information(tokens):
    """Calculates average pointwise mutual information or sequential transition likelihood."""
    if len(tokens) < 2:
        return 0.0
    bigrams = list(zip(tokens[:-1], tokens[1:]))
    n_bigrams = len(bigrams)
    n_unigrams = len(tokens)

    bi_counts = Counter(bigrams)
    uni_counts = Counter(tokens)

    score = 0.0
    for (t1, t2), count in bi_counts.items():
        p_bi = count / n_bigrams
        p1 = uni_counts[t1] / n_unigrams
        p2 = uni_counts[t2] / n_unigrams
        pmi = np.log2(p_bi / (p1 * p2) + 1e-9)
        score += count —
