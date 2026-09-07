"""
voynich-state-viewer: Interactive Streamlit Exploration Dashboard.
Visual Pattern Explorer for Discrete Dynamical State Trajectories (C / L / P / R).
"""

import os
import io
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

from parser import VoynichParser, parse_zl3b, STATE_COLORS, STATE_LABELS

# -----------------------------------------------------------------------------
# Configuration & Theming
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Voynich State Viewer",
    page_icon="📜",
    layout="wide",
    initial_sidebar_state="expanded"
)

DEFAULT_DATA_PATH = os.path.join("data", "ZL3b-n.txt")


@st.cache_data(show_spinner="Parsing IVTFF transliteration corpus...")
def load_corpus_from_path(filepath: str) -> pd.DataFrame:
    """Reads and parses the raw IVTFF file from local disk."""
    return parse_zl3b(filepath)


@st.cache_data(show_spinner="Parsing uploaded transliteration corpus...")
def load_corpus_from_bytes(file_bytes: bytes) -> pd.DataFrame:
    """Handles user-uploaded ZL3b transliteration files."""
    temp_stream = io.StringIO(file_bytes.decode("utf-8", errors="ignore"))
    temp_path = "temp_uploaded_zl3b.txt"
    with open(temp_path, "w", encoding="utf-8") as f:
        f.write(temp_stream.read())
    df = parse_zl3b(temp_path)
    if os.path.exists(temp_path):
        os.remove(temp_path)
    return df


# -----------------------------------------------------------------------------
# UI Rendering Helpers
# -----------------------------------------------------------------------------
def render_legend():
    """Renders the color-coded state legend across uniform horizontal blocks."""
    cols = st.columns(5)
    for col, (state, color) in zip(cols, STATE_COLORS.items()):
        col.markdown(
            f'<div style="background-color:{color}; padding:6px; border-radius:5px; '
            f'text-align:center; color:#000000; font-weight:bold; font-size:13px;">'
            f'{state}: {STATE_LABELS[state]}</div>',
            unsafe_allow_html=True
        )


def render_folio_html(sub_df: pd.DataFrame) -> str:
    """Generates inline HTML spans representing parsed tokens colored by macrostate."""
    html_out = [
        '<div style="font-family:\'Courier New\', monospace; line-height:2.4; '
        'font-size:14px; padding:14px; background:#121212; border-radius:8px; border:1px solid #333;">'
    ]
    current_line = None

    for _, row in sub_df.iterrows():
        if row["header"] != current_line:
            if current_line is not None:
                html_out.append("<br/>")
            current_line = row["header"]
            html_out.append(f'<span style="color:#777; font-size:11px;">[{row["header"]}] </span>')

        color = STATE_COLORS.get(row["state"], "#9E9E9E")
        tooltip = (
            f"Token: {row['token']} | Clean: {row['clean']} | State: {row['state']} | "
            f"Control: {row['control']} | Core: {row['carrier_core']} | Exit: {row['exit_port']}"
        )
        html_out.append(
            f'<span style="background-color:{color}; color:#000000; padding:2px 6px; margin:2px; '
            f'border-radius:3px; font-weight:bold; cursor:default;" title="{tooltip}">'
            f'{row["clean"]}</span> '
        )

    html_out.append('</div>')
    return "".join(html_out)


def render_state_timeline(sub_df: pd.DataFrame):
    """Draws a horizontal continuous color bar of state trajectories."""
    timeline_colors = [STATE_COLORS.get(s, "#9E9E9E") for s in sub_df["state"]]
    if not timeline_colors:
        return

    fig, ax = plt.subplots(figsize=(12, 0.6))
    for i, c in enumerate(timeline_colors):
        ax.barh(0, 1, left=i, color=c, edgecolor='none')
    ax.set_xlim(0, len(timeline_colors))
    ax.axis("off")
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
    st.pyplot(fig)
    plt.close(fig)


# -----------------------------------------------------------------------------
# Main Application Flow
# -----------------------------------------------------------------------------
st.title("Voynich State Viewer")
st.caption("Discrete Dynamical State Machine Explorer (C / L / P / R Architecture)")

# Load Data Pipeline
df = None
if os.path.exists(DEFAULT_DATA_PATH):
    df = load_corpus_from_path(DEFAULT_DATA_PATH)
else:
    st.sidebar.warning("`data/ZL3b-n.txt` not detected in repository.")
    uploaded_file = st.sidebar.file_uploader("Upload ZL3b-n.txt File", type=["txt"])
    if uploaded_file is not None:
        df = load_corpus_from_bytes(uploaded_file.getvalue())

if df is None or df.empty:
    st.info(
        "Please provide an authoritative IVTFF transliteration file (`ZL3b-n.txt`) "
        "by adding it to a `data/` folder or uploading it via the sidebar."
    )
    st.stop()

# Sidebar Navigation
st.sidebar.markdown("---")
st.sidebar.header("Navigation")
folios = sorted([f for f in df["folio"].unique() if f])
view_mode = st.sidebar.radio(
    "Select View Mode",
    ["Single Folio", "Side-by-Side Comparison", "Transition Matrices", "Morphological Feature Audit"]
)

st.sidebar.markdown("---")
st.sidebar.markdown(f"**Total Tokens:** {len(df):,}")
st.sidebar.markdown(f"**Total Folios:** {len(folios)}")
clean_mapped = (df["state"] != "?").mean() * 100
st.sidebar.markdown(f"**Clean Mapped Ratio:** {clean_mapped:.1f}%")


# -----------------------------------------------------------------------------
# VIEW 1: Single Folio Viewer
# -----------------------------------------------------------------------------
if view_mode == "Single Folio":
    selected_folio = st.sidebar.selectbox("Select Folio", folios, index=0)
    sub = df[df["folio"] == selected_folio].copy()

    currier_val = sub["currier"].iloc[0] if not sub.empty else "UNKNOWN"
    quire_val = sub["quire"].iloc[0] if not sub.empty else "UNKNOWN"

    st.subheader(f"Folio `{selected_folio}` (Currier: {currier_val} | Quire: {quire_val})")
    render_legend()
    st.markdown(" ")
    st.markdown(render_folio_html(sub), unsafe_allow_html=True)

    st.markdown("#### State Trajectory Timeline")
    render_state_timeline(sub)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Forward State Trajectory:**")
        st.text(" → ".join(sub["state"].tolist()))
    with col2:
        st.markdown("**State Counts:**")
        st.dataframe(sub["state"].value_counts().to_frame().T, use_container_width=True)


# -----------------------------------------------------------------------------
# VIEW 2: Side-by-Side Comparison
# -----------------------------------------------------------------------------
elif view_mode == "Side-by-Side Comparison":
    st.subheader("Comparative State Architecture")
    render_legend()
    st.markdown(" ")

    col1, col2 = st.columns(2)
    with col1:
        f1 = st.selectbox("Folio A", folios, index=0)
        sub1 = df[df["folio"] == f1]
        st.markdown(f"**Folio {f1}** (Currier: {sub1['currier'].iloc[0]})")
        st.markdown(render_folio_html(sub1), unsafe_allow_html=True)
        render_state_timeline(sub1)

    with col2:
        f2 = st.selectbox("Folio B", folios, index=min(1, len(folios) - 1))
        sub2 = df[df["folio"] == f2]
        st.markdown(f"**Folio {f2}** (Currier: {sub2['currier'].iloc[0]})")
        st.markdown(render_folio_html(sub2), unsafe_allow_html=True)
        render_state_timeline(sub2)


# -----------------------------------------------------------------------------
# VIEW 3: Transition Matrices
# -----------------------------------------------------------------------------
elif view_mode == "Transition Matrices":
    st.subheader("Empirical State Transition Probabilities P(State_{n+1} | State_n)")
    render_legend()
    st.write(" ")

    mode_filter = st.radio("Corpus Scope", ["All Currier Regimes", "Currier A Only", "Currier B Only"], horizontal=True)
    matrix_df = df.copy()

    if mode_filter == "Currier A Only":
        matrix_df = matrix_df[matrix_df["currier"] == "A"]
    elif mode_filter == "Currier B Only":
        matrix_df = matrix_df[matrix_df["currier"] == "B"]

    valid = matrix_df[
        matrix_df["state"].isin(["C", "L", "P", "R"]) & 
        matrix_df["next_state"].isin(["C", "L", "P", "R"])
    ]

    if not valid.empty:
        ct = pd.crosstab(valid["state"], valid["next_state"], normalize="index")
        states_order = [s for s in ["C", "L", "P", "R"] if s in ct.index]
        ct = ct.reindex(index=states_order, columns=states_order, fill_value=0.0)

        fig, ax = plt.subplots(figsize=(6, 4.5))
        sns.heatmap(ct, annot=True, fmt=".3f", cmap="Blues", cbar=True, ax=ax, linewidths=0.5)
        ax.set_xlabel("Next State (n+1)")
        ax.set_ylabel("Current State (n)")
        ax.set_title(f"Transition Matrix: {mode_filter}")
        st.pyplot(fig)
        plt.close(fig)
    else:
        st.warning("Insufficient sequential transitions available for the selected filter.")


# -----------------------------------------------------------------------------
# VIEW 4: Morphological Feature Audit
# -----------------------------------------------------------------------------
elif view_mode == "Morphological Feature Audit":
    st.subheader("Token Decomposition Feature Table")
    display_cols = [
        "folio", "header", "currier", "token", "clean", 
        "control", "carrier_core", "e_grade", "exit_port", "state", "is_line_end"
    ]
    st.dataframe(df[display_cols].head(150), use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.write("#### Successor Exit Port Distribution (rho)")
        st.bar_chart(df["exit_port"].value_counts())

    with col2:
        st.write("#### Control Header Distribution (C)")
        st.bar_chart(df["control"].value_counts())
