import os
import re
import urllib.request
from collections import Counter
import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Voynich Decipherment Workbench", layout="wide")

DATA_PATH = "data/ZL3b-n.txt"
FALLBACK_URL = "https://www.voynich.nu/data/ZL3b-n.txt"

# -----------------------------------------------------------------------------
# 1. Corpus Loader
# -----------------------------------------------------------------------------
@st.cache_data(show_spinner="Ingesting Voynich Transliteration Corpus...")
def load_corpus_tokens():
    raw_text = ""
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, "r", encoding="utf-8", errors="ignore") as f:
            raw_text = f.read()
    else:
        req = urllib.request.Request(FALLBACK_URL, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req) as resp:
            raw_text = resp.read().decode("utf-8", errors="ignore")

    tokens = []
    lines = []
    for line in raw_text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        clean_line = re.sub(r"<[^>]+>", "", line)
        parts = re.split(r"[.,\s]+", clean_line)
        line_tokens = [re.sub(r"[^a-z0-9]", "", p.lower()) for p in parts if p]
        line_tokens = [tok for tok in line_tokens if tok]
        if line_tokens:
            tokens.extend(line_tokens)
            lines.append({"header": line.split()[0] if line.startswith("<") else "locus", "tokens": line_tokens})
    return tokens, lines

# -----------------------------------------------------------------------------
# 2. Sukhotin Vowel Induction Algorithm
# -----------------------------------------------------------------------------
@st.cache_data
def run_sukhotin(tokens):
    char_counts = Counter("".join(tokens))
    alphabet = sorted([c for c, cnt in char_counts.items() if cnt >= 10 and c.isalpha()])
    c2i = {c: i for i, c in enumerate(alphabet)}
    n = len(alphabet)

    M = np.zeros((n, n), dtype=int)
    for tok in tokens:
        for c1, c2 in zip(tok[:-1], tok[1:]):
            if c1 in c2i and c2 in c2i:
                i, j = c2i[c1], c2i[c2]
                M[i, j] += 1
                M[j, i] += 1

    V = set()
    freq = {c: char_counts[c] for c in alphabet}

    while True:
        scores = {}
        for c in alphabet:
            if c in V:
                continue
            i = c2i[c]
            non_vowel_contacts = sum(M[i, c2i[c_prime]] for c_prime in alphabet if c_prime not in V)
            scores[c] = 2 * non_vowel_contacts - freq[c]

        best_c, best_val = max(scores.items(), key=lambda x: x[1])
        if best_val <= 0:
            break
        V.add(best_c)

    consonants = sorted([c for c in alphabet if c not in V])
    vowels = sorted(list(V))
    return vowels, consonants, freq, alphabet, M

# -----------------------------------------------------------------------------
# 3. Streamlit Interface
# -----------------------------------------------------------------------------
st.title("Voynich Manuscript Decipherment & Sukhotin Induction")

tokens, lines = load_corpus_tokens()
st.caption(f"Corpus loaded: {len(tokens):,} word tokens across {len(lines):,} transcription lines.")

tabs = st.tabs(["🔤 1. Sukhotin Phonetics", "📖 2. Parallel Folio Reader", "📜 3. Corpus Tokens"])

# Tab 1: Sukhotin Vowel Induction
with tabs[0]:
    st.subheader("Sukhotin Vowel-Consonant Induction Benchmark")
    st.markdown(
        "Mathematically separates consonants from vocalic nuclei using character adjacency contact matrices "
        "without prior phonetic or linguistic assumptions."
    )

    vowels, consonants, freq, alphabet, M = run_sukhotin(tokens)

    total_chars = sum(freq.values())
    vowel_vol = sum(freq[c] for c in vowels)
    vowel_ratio = (vowel_vol / total_chars) * 100 if total_chars else 0

    col1, col2, col3 = st.columns(3)
    col1.metric("Deduced Vocalic Set (V)", ", ".join(vowels))
    col2.metric("Consonantal Count", len(consonants))
    col3.metric("Corpus Vowel Volume", f"{vowel_ratio:.2f}%")

    st.markdown("---")
    st.markdown("#### Phonotactic Evaluation")
    if 30.0 <= vowel_ratio <= 45.0:
        st.success(f"Vowel density of {vowel_ratio:.2f}% is within the natural European Romance/Latin phonotactic range (30%–45%).")
    else:
        st.info(f"Vowel density computed: {vowel_ratio:.2f}%.")

    st.markdown("#### Character Frequency & Partition Breakdown")
    data_rows = []
    for c in alphabet:
        data_rows.append({
            "Character": c,
            "Class": "Vowel (Nucleus)" if c in vowels else "Consonant",
            "Frequency": freq[c],
            "Relative Share (%)": f"{(freq[c] / total_chars) * 100:.2f}%"
        })
    df_chars = pd.DataFrame(data_rows).sort_values(by="Frequency", ascending=False)
    st.dataframe(df_chars, use_container_width=True)

# Tab 2: Parallel Folio Reader
with tabs[1]:
    st.subheader("Corpus Line Browser")
    st.write(f"Displaying sample transcription lines from the loaded corpus:")
    sample_lines = lines[:50]
    for row in sample_lines:
        st.markdown(f"**Line:** `{row['header']}` &nbsp;|&nbsp; `{' '.join(row['tokens'])}`")

# Tab 3: Raw Tokens
with tabs[2]:
    st.subheader("High-Frequency Corpus Tokens")
    top_toks = Counter(tokens).most_common(50)
    df_toks = pd.DataFrame(top_toks, columns=["Token", "Count"])
    st.dataframe(df_toks, use_container_width=True)
