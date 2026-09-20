import streamlit as st
import pandas as pd
import numpy as np
import math
import re
from collections import Counter
import altair as alt

st.set_page_config(
    page_title="Voynich Decipherment Workbench",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# CORE ANALYTICAL FUNCTIONS
# ---------------------------------------------------------

def clean_eva_tokens(raw_text: str):
    """Clean and tokenize EVA-transcribed Voynich text."""
    text = re.sub(r"<[^>]+>", "", raw_text)
    text = re.sub(r"[!=?,;:\$#@*]", "", text)
    tokens = [t.strip().lower() for t in re.split(r"[\s\.\-]+", text) if t.strip()]
    return tokens

def calculate_shannon_entropy(tokens, level="char"):
    """Calculate Shannon Entropy in bits for characters or tokens."""
    if not tokens:
        return 0.0
    if level == "char":
        units = "".join(tokens)
    else:
        units = tokens

    total = len(units)
    if total == 0:
        return 0.0
    
    counts = Counter(units)
    entropy = -sum((count / total) * math.log2(count / total) for count in counts.values())
    return round(entropy, 4)

def get_ngram_frequencies(tokens, n=2, level="char"):
    """Compute n-gram frequencies for characters or words."""
    ngrams = []
    if level == "char":
        for token in tokens:
            if len(token) >= n:
                for i in range(len(token) - n + 1):
                    ngrams.append(token[i:i+n])
    else:
        if len(tokens) >= n:
            for i in range(len(tokens) - n + 1):
                ngrams.append(" ".join(tokens[i:i+n]))
    return Counter(ngrams)

def analyze_character_positions(tokens):
    """Examine character frequency by word position: initial, medial, final."""
    initials = Counter()
    medials = Counter()
    finals = Counter()
    
    for token in tokens:
        if len(token) == 1:
            initials[token] += 1
            finals[token] += 1
        elif len(token) == 2:
            initials[token[0]] += 1
            finals[token[1]] += 1
        else:
            initials[token[0]] += 1
            finals[token[-1]] += 1
            for char in token[1:-1]:
                medials[char] += 1
                
    chars = sorted(list(set(initials.keys()) | set(medials.keys()) | set(finals.keys())))
    data = []
    for c in chars:
        data.append({
            "Glyph": c,
            "Initial": initials[c],
            "Medial": medials[c],
            "Final": finals[c],
            "Total": initials[c] + medials[c] + finals[c]
        })
    df = pd.DataFrame(data)
    if not df.empty:
        return df.sort_values(by="Total", ascending=False)
    return pd.DataFrame(columns=["Glyph", "Initial", "Medial", "Final", "Total"])

def apply_substitution(tokens, mapping):
    """Replace EVA characters or n-graphs based on user hypothesis mapping."""
    if not mapping or not tokens:
        return tokens

    sorted_keys = sorted(mapping.keys(), key=len, reverse=True)
    pattern = re.compile("|".join(re.escape(k) for k in sorted_keys))

    substituted = []
    for token in tokens:
        translated = pattern.sub(lambda m: mapping[m.group(0)], token)
        substituted.append(translated)
    return substituted

# ---------------------------------------------------------
# UI & WORKBENCH LAYOUT
# ---------------------------------------------------------

st.title("Voynich Analysis & Decipherment Workbench")
st.caption("Information Theory, Frequency Distributions, and Hypothesis Testing")

sidebar = st.sidebar
sidebar.header("Input Data")

sample_eva = """
fachys ykal ar ataiin shol shory cthephos ychey rshey
qokain ol chedy qokedy chedy chey keol cheol
daiin daiin cthey shey or aiin chal ar chor
cthor shey qokeey dain qokal ctheor chckhy
"""

input_mode = sidebar.radio("Data Source", ["Sample Text", "Paste Raw EVA", "Upload File"])

if input_mode == "Sample Text":
    raw_input = sample_eva
elif input_mode == "Paste Raw EVA":
    raw_input = sidebar.text_area("Paste EVA / Currier Transcript Here", height=250)
else:
    uploaded = sidebar.file_uploader("Upload .txt file", type=["txt"])
    raw_input = uploaded.read().decode("utf-8") if uploaded else ""

tokens = clean_eva_tokens(raw_input)

# Metrics Ribbon
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Word Tokens", len(tokens))
col2.metric("Unique Word Tokens", len(set(tokens)))
col3.metric("Char Entropy (H)", f"{calculate_shannon_entropy(tokens, 'char')} bits")
col4.metric("Word Entropy (H)", f"{calculate_shannon_entropy(tokens, 'word')} bits")

st.divider()

# Tab Navigation
tab_pos, tab_ngrams, tab_currier, tab_cipher = st.tabs([
    "Positional Rules",
    "N-Gram & Frequency",
    "Currier A vs B Flags",
    "Substitution Sandbox"
])

# ---------------------------------------------------------
# TAB 1: POSITIONAL RULES
# ---------------------------------------------------------
with tab_pos:
    st.subheader("Glyph Positional Distribution (Initial vs. Medial vs. Final)")
    st.write("Identifies strictly positional characters (e.g., gallows characters like `t`, `p`, `k`, `f` vs. suffixes like `y`, `n`).")
    
    if tokens:
        pos_df = analyze_character_positions(tokens)
        
        if not pos_df.empty:
            max_glyphs = min(35, len(pos_df))
            top_n = st.slider("Top Glyphs to Display", min_value=1, max_value=max_glyphs, value=min(15, max_glyphs))
            top_pos = pos_df.head(top_n)
            
            glyph_order = top_pos["Glyph"].tolist()
            
            melted_pos = top_pos.melt(
                id_vars=["Glyph"], 
                value_vars=["Initial", "Medial", "Final"], 
                var_name="Position", 
                value_name="Count"
            )
            
            # Grouped bar chart with xOffset for distinct side-by-side columns
            chart = alt.Chart(melted_pos).mark_bar().encode(
                x=alt.X("Glyph:N", sort=glyph_order, axis=alt.Axis(title="Glyph", labelAngle=0)),
                y=alt.Y("Count:Q", axis=alt.Axis(title="Occurrences")),
                color=alt.Color(
                    "Position:N", 
                    scale=alt.Scale(domain=["Initial", "Medial", "Final"], range=["#4C78A8", "#F58518", "#54A24B"])
                ),
                xOffset=alt.XOffset("Position:N", sort=["Initial", "Medial", "Final"]),
                tooltip=["Glyph", "Position", "Count"]
            ).properties(
                height=380
            ).interactive()
            
            st.altair_chart(chart, use_container_width=True)
            st.dataframe(top_pos, use_container_width=True)
        else:
            st.warning("No glyphs detected in the input.")
    else:
        st.info("Input text to view positional rules.")

# ---------------------------------------------------------
# TAB 2: N-GRAM & FREQUENCY
# ---------------------------------------------------------
with tab_ngrams:
    st.subheader("Frequency Analysis")
    sub_col1, sub_col2 = st.columns([1, 2])
    
    with sub_col1:
        ngram_level = st.selectbox("Unit", ["char", "word"])
        n_val = st.slider("N-Gram Length (N)", 1, 4, 2)
        top_k = st.slider("Results to Show", 10, 50, 20)
        
    with sub_col2:
        if tokens:
            ngrams = get_ngram_frequencies(tokens, n=n_val, level=ngram_level)
            if ngrams:
                ngram_df = pd.DataFrame(ngrams.most_common(top_k), columns=["N-Gram", "Frequency"])
                
                bar_chart = alt.Chart(ngram_df).mark_bar().encode(
                    x=alt.X("Frequency:Q"),
                    y=alt.Y("N-Gram:N", sort="-x"),
                    tooltip=["N-Gram", "Frequency"]
                ).properties(height=400)
                
                st.altair_chart(bar_chart, use_container_width=True)
                st.dataframe(ngram_df, use_container_width=True)
            else:
                st.warning("Not enough units to generate n-grams of this length.")
        else:
            st.info("Input text to view n-gram frequencies.")

# ---------------------------------------------------------
# TAB 3: CURRIER A vs. B SEPARATION
# ---------------------------------------------------------
with tab_currier:
    st.subheader("Currier Dialect Split Detector")
    st.write("Measures marker tokens that typically distinguish Currier A (herbal/simple) from Currier B (balneological/complex).")
    
    currier_a_markers = {"daiin", "chol", "chor", "shol", "cthor"}
    currier_b_markers = {"chedy", "shedy", "qokedy", "qokain", "chey"}
    
    token_set = Counter(tokens)
    a_count = sum(token_set[word] for word in currier_a_markers)
    b_count = sum(token_set[word] for word in currier_b_markers)
    total_markers = a_count + b_count
    
    c_col1, c_col2 = st.columns(2)
    with c_col1:
        st.metric("Currier A Signature Count", a_count)
        for w in sorted(currier_a_markers):
            st.write(f"- `{w}`: {token_set[w]}")
            
    with c_col2:
        st.metric("Currier B Signature Count", b_count)
        for w in sorted(currier_b_markers):
            st.write(f"- `{w}`: {token_set[w]}")
            
    if total_markers > 0:
        ratio_b = round((b_count / total_markers) * 100, 1)
        st.progress(ratio_b / 100)
        st.caption(f"Dialect Lean: {round(100 - ratio_b, 1)}% Currier A | {ratio_b}% Currier B")
    else:
        st.info("No standard Currier A or Currier B index tokens found in this excerpt.")

# ---------------------------------------------------------
# TAB 4: SUBSTITUTION SANDBOX
# ---------------------------------------------------------
with tab_cipher:
    st.subheader("Interactive Substitution Cipher Sandbox")
    st.write("Map EVA characters or n-graphs to test languages (Latin, Italian, Hebrew transliteration, etc.).")
    
    mapping_str = st.text_input(
        "Mapping dictionary (comma separated, e.g., o:a, l:r, d:t, ch:s, cth:t)",
        value="o:a, l:r, d:t, ch:s"
    )
    
    mapping = {}
    if mapping_str.strip():
        for pair in mapping_str.split(","):
            if ":" in pair:
                parts = pair.split(":")
                k = parts[0].strip().lower()
                v = parts[1].strip()
                if k:
                    mapping[k] = v
                
    st.write("Active Mapping:", mapping)
    
    if tokens:
        transformed = apply_substitution(tokens, mapping)
        st.markdown("**Transformed Text Stream:**")
        preview_limit = 200
        preview = " ".join(transformed[:preview_limit])
        if len(transformed) > preview_limit:
            preview += "..."
        st.code(preview, language="text")
    else:
        st.info("Input text to view transformed output.")
