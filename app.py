import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from collections import Counter
import math

st.set_page_config(page_title="Voynich Analysis & Decipherment Workbench", layout="wide")

# Embedded sample Voynich EVA transcription lines (Currier A and B samples)
DEFAULT_VOYNICH_TEXT = """
fachys ykal ar ataiin shol shory cthees ar taiin cthy daiin chor cphaiin
fachys ykal ar ataiin shol shory cthees ar taiin cthy daiin chor cphaiin
otaiin shey or aiin shol daiin ctho cthees chor taiin cphaiin or aiin
s aiin shey daiin chol chol cthaiin cthees daiin shey cphaiin otar aiin
daiin shey or cheor chey chol daiin shey cheor cphaiin otaiin chey shey
qokaiin chol kcheor daiin shey cphaiin or shey chol cthaiin daiin chey
qokor shey kchor taiin shey kcheor cphaiin otar shey chol daiin shey
ytedy qokedy shedaiin qokedy sheor sheor qokain cheor daiin sheor cphain
daiin cheor qokaiin dary daiin cphaiin chey qokain or sheor cphaiin
chedy qokaiin shey chor cphaiin otaiin sheor qokain daiin shey cphaiin
qokedy cheor shey cheor cphaiin qokaiin sheor chey sheor cphaiin
dair cheor shey cphaiin otaiin sheor qokain daiin shey cphaiin
""".strip()

st.title("Voynich Analysis & Decipherment Workbench")
st.caption("Information Theory, Frequency Distributions, and Hypothesis Testing")

# Allow file upload or default fallback
uploaded_file = st.sidebar.file_uploader("Upload EVA Transcription (.txt)", type=["txt"])
if uploaded_file is not None:
    raw_text = uploaded_file.read().decode("utf-8")
else:
    raw_text = DEFAULT_VOYNICH_TEXT

# Tokenize words
words = [w.strip() for w in raw_text.replace("\n", " ").split(" ") if w.strip()]
chars = [c for c in "".join(words)]

# Metrics Calculation
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

# Top KPI row
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Word Tokens", f"{total_tokens:,}")
c2.metric("Unique Word Tokens", f"{unique_tokens:,}")
c3.metric("Char Entropy (H)", f"{char_entropy:.3f} bits")
c4.metric("Word Entropy (H)", f"{word_entropy:.3f} bits")

st.markdown("---")

tab1, tab2, tab3, tab4 = st.tabs(["Positional Rules", "N-Gram & Frequency", "Currier A vs B Flags", "Substitution Sandbox"])

with tab1:
    st.subheader("Glyph Positional Distribution (Initial vs. Medial vs. Final)")
    st.caption("Identifies positional preferences (e.g., initial gallows characters vs. suffixes like y, n).")

    col_ctrl1, col_ctrl2 = st.columns([1, 1])
    with col_ctrl1:
        top_n = st.slider("Top Glyphs to Display", min_value=3, max_value=25, value=15)
    with col_ctrl2:
        chart_mode = st.radio("Chart Type", ["Stacked Total", "100% Normalized (%)"], horizontal=True)

    # Calculate positions
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

    plot_rows = []
    for g in common_glyphs:
        init_cnt = glyph_initial[g]
        med_cnt = glyph_medial[g]
        fin_cnt = glyph_final[g]
        total = init_cnt + med_cnt + fin_cnt

        if chart_mode == "100% Normalized (%)" and total > 0:
            plot_rows.append({"Glyph": g, "Position": "Initial", "Frequency": (init_cnt / total) * 100})
            plot_rows.append({"Glyph": g, "Position": "Medial", "Frequency": (med_cnt / total) * 100})
            plot_rows.append({"Glyph": g, "Position": "Final", "Frequency": (fin_cnt / total) * 100})
        else:
            plot_rows.append({"Glyph": g, "Position": "Initial", "Frequency": init_cnt})
            plot_rows.append({"Glyph": g, "Position": "Medial", "Frequency": med_cnt})
            plot_rows.append({"Glyph": g, "Position": "Final", "Frequency": fin_cnt})

    df_pos = pd.DataFrame(plot_rows)

    if not df_pos.empty:
        fig = px.bar(
            df_pos,
            x="Glyph",
            y="Frequency",
            color="Position",
            barmode="stack",
            color_discrete_map={"Initial": "#3b82f6", "Medial": "#10b981", "Final": "#f59e0b"},
            height=450
        )
        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor="#334155")
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No character data found to display.")

with tab2:
    st.subheader("Word Frequency Distribution")
    word_freq = Counter(words).most_common(20)
    df_words = pd.DataFrame(word_freq, columns=["Word", "Count"])
    st.bar_chart(df_words.set_index("Word"))

with tab3:
    st.subheader("Currier Classification Flags")
    st.write("Upload a complete transcriber interlinear file (EVA format) to run Currier A / Currier B separation.")

with tab4:
    st.subheader("Substitution Sandbox")
    sample_phrase = " ".join(words[:12])
    st.text_area("Input Sample", value=sample_phrase, height=70)
