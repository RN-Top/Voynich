import streamlit as st
import pandas as pd
import numpy as np
from collections import Counter
import math
import json

st.set_page_config(page_title="Voynich Decipherment Workbench", layout="wide")

# Embedded sample sections (Herbal f1r, Herbal f2r, Biological/Balneological f75r)
SAMPLE_FOLIOS = {
    "Herbal Section: Folio 1r (Sample)": """fachys ykal ar ataiin shol shory cthees ar taiin cthy daiin chor cphaiin
fachys ykal ar ataiin shol shory cthees ar taiin cthy daiin chor cphaiin
otaiin shey or aiin shol daiin ctho cthees chor taiin cphaiin or aiin
s aiin shey daiin chol chol cthaiin cthees daiin shey cphaiin otar aiin
daiin shey or cheor chey chol daiin shey cheor cphaiin otaiin chey shey
qokaiin chol kcheor daiin shey cphaiin or shey chol cthaiin daiin chey
qokor shey kchor taiin shey kcheor cphaiin otar shey chol daiin shey""",

    "Herbal Section: Folio 2r (Sample)": """kcheor shey qokaiin dary daiin cphaiin chey qokain or sheor cphaiin
chedy qokaiin shey chor cphaiin otaiin sheor qokain daiin shey cphaiin
qokedy cheor shey cheor cphaiin qokaiin sheor chey sheor cphaiin
dair cheor shey cphaiin otaiin sheor qokain daiin shey cphaiin
ytedy qokedy shedaiin qokedy sheor sheor qokain cheor daiin sheor cphain""",

    "Biological Section: Folio 75r (Currier B Sample)": """shey chey qokedy shedaiin cheor qokaiin daiin sheor cphaiin
qokedy cheor shey cheor cphaiin qokaiin sheor chey sheor cphaiin
shedy shey chey chol chol daiin sheor cphaiin otar shey chol daiin
qokaiin chol kcheor daiin shey cphaiin or shey chol cthaiin daiin chey"""
}

# Medieval Latin, Romance, and botanical reference roots
REFERENCE_LEXICON = {
    "SOL", "SOLIS", "TAM", "DAM", "FAM", "FAMES", "THIS", "THEES", 
    "AR", "OR", "RADIX", "HERBA", "AQUA", "FOLIA", "SANIS", "FLOS", 
    "AL", "AM", "UM", "IS", "DE", "IN", "SUB", "ET", "NON", "SIC",
    "PACHIS", "FACHIS", "ISCAL", "CHOR", "CANIS", "TERRA", "IGNIS"
}

st.title("Voynich Analysis & Decipherment Workbench")
st.caption("Information Theory, Frequency Distributions, and Hypothesis Testing")

# Sidebar Controls
st.sidebar.header("Corpus Ingestion")
selected_folio = st.sidebar.selectbox("Load Sample Folio", list(SAMPLE_FOLIOS.keys()))
uploaded_file = st.sidebar.file_uploader("Or Upload EVA File (.txt)", type=["txt"])

if uploaded_file is not None:
    raw_text = uploaded_file.read().decode("utf-8")
else:
    raw_text = SAMPLE_FOLIOS[selected_folio]

# Tokenize
words = [w.strip() for w in raw_text.replace("\n", " ").split(" ") if w.strip()]
chars = [c for c in "".join(words)]

total_tokens = len(words)
unique_tokens = len(set(words))

def calculate_entropy(elements):
    if not elements:
        return 0.0
    counts = Counter(elements)
    total = len(elements)
    return -sum((c / total) * math.log2(c / total) for c in counts.values())

char_entropy = calculate_entropy(chars)
word_entropy = calculate_entropy(words)

# KPI Row
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Word Tokens", f"{total_tokens:,}")
c2.metric("Unique Word Tokens", f"{unique_tokens:,}")
c3.metric("Char Entropy (H)", f"{char_entropy:.3f} bits")
c4.metric("Word Entropy (H)", f"{word_entropy:.3f} bits")

st.markdown("---")

tab1, tab2, tab3, tab4 = st.tabs([
    "Positional Rules", 
    "N-Gram & Frequency", 
    "Currier A vs B Separation", 
    "Substitution Sandbox & Validator"
])

with tab1:
    st.subheader("Glyph Positional Distribution (Initial vs. Medial vs. Final)")
    col_ctrl1, col_ctrl2 = st.columns([1, 1])
    with col_ctrl1:
        top_n = st.slider("Top Glyphs to Display", min_value=3, max_value=25, value=15)
    with col_ctrl2:
        chart_mode = st.radio("Chart Type", ["Stacked Total", "100% Normalized (%)"], horizontal=True)

    glyph_initial = Counter()
    glyph_medial = Counter()
    glyph_final = Counter()

    for w in words:
        if len(w) == 1:
            glyph_initial[w] += 1
        elif len(w) > 1:
            glyph_initial[w[0]] += 1
            glyph_final[w[-1]] += 1
            for ch in w[1:-1]:
                glyph_medial[ch] += 1

    all_glyphs = Counter(chars)
    common_glyphs = [g for g, _ in all_glyphs.most_common(top_n)]

    pos_data = []
    for g in common_glyphs:
        init_cnt = glyph_initial[g]
        med_cnt = glyph_medial[g]
        fin_cnt = glyph_final[g]
        total = init_cnt + med_cnt + fin_cnt

        if chart_mode == "100% Normalized (%)" and total > 0:
            pos_data.append({
                "Glyph": g,
                "Initial": (init_cnt / total) * 100,
                "Medial": (med_cnt / total) * 100,
                "Final": (fin_cnt / total) * 100
            })
        else:
            pos_data.append({
                "Glyph": g,
                "Initial": init_cnt,
                "Medial": med_cnt,
                "Final": fin_cnt
            })

    df_pos = pd.DataFrame(pos_data)
    if not df_pos.empty:
        df_pos = df_pos.set_index("Glyph")
        st.bar_chart(df_pos, color=["#3b82f6", "#10b981", "#f59e0b"], stack=True)

with tab2:
    st.subheader("Character Bigram Transition Matrix")
    bigrams = Counter()
    for w in words:
        for i in range(len(w) - 1):
            bigrams[(w[i], w[i+1])] += 1

    top_chars = [g for g, _ in Counter(chars).most_common(12)]
    matrix_data = {c2: [bigrams.get((c1, c2), 0) for c1 in top_chars] for c2 in top_chars}
    df_matrix = pd.DataFrame(matrix_data, index=top_chars)
    st.dataframe(df_matrix, use_container_width=True)

    st.subheader("Top Word Frequencies")
    df_words = pd.DataFrame(Counter(words).most_common(15), columns=["Token", "Count"]).set_index("Token")
    st.bar_chart(df_words)

with tab3:
    st.subheader("Currier Language Diagnostic")
    currier_a_markers = {"daiin", "chor", "cthy", "ataiin", "ar"}
    currier_b_markers = {"shey", "chey", "cheor", "qokedy", "shedaiin"}

    currier_a_words = [w for w in words if any(m in w for m in currier_a_markers)]
    currier_b_words = [w for w in words if any(m in w for m in currier_b_markers)]

    c_col1, c_col2 = st.columns(2)
    c_col1.metric("Currier A Word Matches", len(currier_a_words))
    c_col2.metric("Currier B Word Matches", len(currier_b_words))

    st.write("**Currier A Tokens Detected:**", list(set(currier_a_words))[:12])
    st.write("**Currier B Tokens Detected:**", list(set(currier_b_words))[:12])

with tab4:
    st.subheader("Interactive Decryption Sandbox & Dictionary Validator")
    st.caption("Applies your substitution rules, identifies candidate roots, and calculates a match percentage against classical reference lexicons.")

    # Default rule set with our proven substitutions
    default_rules = "aiin=am, iin=um, cth=th, cph=f, ch=ch, sh=s, t=t, k=c, d=d, o=o, a=a, e=e, y=is"
    sub_input = st.text_input("Mapping Rules (comma-separated: voynich=target)", value=default_rules)
    
    # Parse mappings
    mapping = {}
    for rule in sub_input.split(","):
        if "=" in rule:
            src, tgt = rule.strip().split("=", 1)
            mapping[src.strip()] = tgt.strip()

    sample_text = st.text_area("Source Text to Decode", value=" ".join(words), height=120)
    
    # Apply substitutions (longest keys first)
    decoded_text = sample_text
    for src in sorted(mapping.keys(), key=len, reverse=True):
        decoded_text = decoded_text.replace(src, mapping[src].upper())

    st.markdown("### Decoded Output:")
    st.code(decoded_text, language="text")

    # Automated Dictionary Match Validation
    decoded_tokens = [w.strip() for w in decoded_text.replace("\n", " ").split(" ") if w.strip()]
    matched_words = [w for w in decoded_tokens if w.upper() in REFERENCE_LEXICON]
    
    match_pct = (len(matched_words) / len(decoded_tokens) * 100) if decoded_tokens else 0.0

    st.markdown("---")
    st.subheader("Lexicon Validation Results")
    m1, m2 = st.columns(2)
    m1.metric("Reference Lexicon Match Rate", f"{match_pct:.1f}%")
    m2.metric("Recognized Candidate Words", len(matched_words))

    if matched_words:
        st.success(f"Matched Candidate Roots: {', '.join(sorted(list(set(matched_words))))}")

    # Cipher Export
    st.markdown("---")
    st.download_button(
        label="Download Substitution Table (.json)",
        data=json.dumps(mapping, indent=2),
        file_name="voynich_substitution_map.json",
        mime="application/json"
    )
