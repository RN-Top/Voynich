"""
voynich-state-viewer: Interactive Streamlit Exploration Dashboard.
Visual Pattern Explorer for Discrete Dynamical State Trajectories (C / L / P / R)
and Grounded Semantic Analysis Engine.
"""

import os
import io
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

from parser import VoynichParser, parse_zl3b, STATE_COLORS, STATE_LABELS
from analyzer import DeciphermentEngine

# -----------------------------------------------------------------------------
# Configuration & Theming
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Voynich State & Decipherment Engine",
    page_icon="📜",
    layout="wide",
    initial_sidebar_state="expanded"
)

DEFAULT_DATA_PATH = os.path.join("data", "ZL3b-n.txt")


@st.cache_data(show_spinner="Parsing IVTFF transliteration corpus...")
def load_corpus_from_path(filepath: str) -> pd.DataFrame:
    return parse_zl3b(filepath)


@st.cache_data(show_spinner="Parsing uploaded transliteration corpus...")
def load_corpus_from_bytes(file_bytes: bytes) -> pd.DataFrame:
    temp_stream = io.StringIO(file_bytes.decode("utf-8", errors="ignore"))
    temp_path = "temp_uploaded_zl3b.txt"
    with open(temp_path, "w", encoding="utf-8") as f:
        f.write(temp_stream.read())
    df = parse_zl3b(temp_path)
    if os.path.exists(temp_path):
        os.remove(temp_path)
    return df


def render_legend():
    cols = st.columns(5)
    for col, (state, color) in zip(cols, STATE_COLORS.items()):
        col.markdown(
            f'<div style="background-color:{color}; padding:6px; border-radius:5px; '
            f'text-align:center; color:#000000; font-weight:bold; font-size:13px;">'
            f'{state}: {STATE_LABELS[state]}</div>',
            unsafe_allow_html=True
        )


def render_folio_html(sub_df: pd.DataFrame) -> str:
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
            f"Core: {row['carrier_core']} | Port: {row['exit_port']}"
        )
        html_out.append(
            f'<span style="background-color:{color}; color:#000000; padding:2px 6px; margin:2px; '
            f'border-radius:3px; font-weight:bold; cursor:default;" title="{tooltip}">'
            f'{row["clean"]}</span> '
        )

    html_out.append('</div>')
    return "".join(html_out)


def render_state_timeline(sub_df: pd.DataFrame):
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
st.title("Voynich State & Decipherment Engine")
st.caption("Grounded Morphotactic State Machine and Carrier Analysis Suite")

df = None
if os.path.exists(DEFAULT_DATA_PATH):
    df = load_corpus_from_path(DEFAULT_DATA_PATH)
else:
    st.sidebar.warning("`data/ZL3b-n.txt` not detected in repository.")
    uploaded_file = st.sidebar.file_uploader("Upload ZL3b-n.txt File", type=["txt"])
    if uploaded_file is not None:
        df = load_corpus_from_bytes(uploaded_file.getvalue())

if df is None or df.empty:
    st.info("Provide an IVTFF file (`data/ZL3b-n.txt`) or upload via the sidebar to begin.")
    st.stop()

engine = DeciphermentEngine(df)

# Sidebar Navigation
st.sidebar.markdown("---")
st.sidebar.header("Mode Selection")
view_mode = st.sidebar.radio(
    "Select Mode",
    [
        "Single Folio Viewer",
        "Side-by-Side Comparison",
        "Slot Omega Discovery",
        "Domain Specificity (PMI)",
        "Successor Routing (A4)",
        "Token Decomposition Matrix"
    ]
)

folios = sorted([f for f in df["folio"].unique() if f])
st.sidebar.markdown("---")
st.sidebar.markdown(f"**Total Tokens:** {len(df):,}")
st.sidebar.markdown(f"**Total Folios:** {len(folios)}")
clean_mapped = (df["state"] != "?").mean() * 100
st.sidebar.markdown(f"**Mapped State Ratio:** {clean_mapped:.1f}%")

# -----------------------------------------------------------------------------
# 1. Single Folio Viewer
# -----------------------------------------------------------------------------
if view_mode == "Single Folio Viewer":
    selected_folio = st.sidebar.selectbox("Select Folio", folios, index=0)
    sub = df[df["folio"] == selected_folio].copy()

    currier_val = sub["currier"].iloc[0] if not sub.empty else "UNKNOWN"
    section_val = sub["section"].iloc[0] if not sub.empty else "UNKNOWN"

    st.subheader(f"Folio `{selected_folio}` (Currier: {currier_val} | Section: {section_val})")
    render_legend()
    st.markdown(" ")
    st.markdown(render_folio_html(sub), unsafe_allow_html=True)

    st.markdown("#### State Trajectory Timeline")
    render_state_timeline(sub)

# -----------------------------------------------------------------------------
# 2. Side-by-Side Comparison
# -----------------------------------------------------------------------------
elif view_mode == "Side-by-Side Comparison":
    st.subheader("Side-by-Side Folio Comparison")
    render_legend()
    st.markdown(" ")

    col1, col2 = st.columns(2)
    with col1:
        f1 = st.selectbox("Folio Left", folios, index=0)
        sub1 = df[df["folio"] == f1]
        st.markdown(f"**Folio {f1}** (Currier: {sub1['currier'].iloc[0]} | {sub1['section'].iloc[0]})")
        st.markdown(render_folio_html(sub1), unsafe_allow_html=True)
        render_state_timeline(sub1)

    with col2:
        f2 = st.selectbox("Folio Right", folios, index=min(1, len(folios) - 1))
        sub2 = df[df["folio"] == f2]
        st.markdown(f"**Folio {f2}** (Currier: {sub2['currier'].iloc[0]} | {sub2['section'].iloc[0]})")
        st.markdown(render_folio_html(sub2), unsafe_allow_html=True)
        render_state_timeline(sub2)

# -----------------------------------------------------------------------------
# 3. Slot Omega Discovery
# -----------------------------------------------------------------------------
elif view_mode == "Slot Omega Discovery":
    st.subheader("Syntactic Slot Omega Discovery: Q-ACTIVE -> [ X-AIIN ] -> Q-ACTIVE")
    st.markdown(
        "Isolates tokens that occupy the canonical syntactic frame between active Q-control tokens. "
        "Carriers that substitute into this slot without breaking frame syntax are distributional peers."
    )
    omega_df = engine.find_slot_omega_candidates()
    if not omega_df.empty:
        st.dataframe(omega_df, use_container_width=True)
    else:
        st.warning("No Slot Omega occurrences found in the currently loaded folios.")

# -----------------------------------------------------------------------------
# 4. Domain Specificity (PMI)
# -----------------------------------------------------------------------------
elif view_mode == "Domain Specificity (PMI)":
    st.subheader("Pointwise Mutual Information: Carrier Core (Lambda) vs Illustrated Section")
    st.markdown(
        "Values **> 0** indicate that a carrier stem appears in a section far more frequently than chance. "
        "This grounds morphological stems in subject domains without projecting unverified English meanings."
    )
    min_occ = st.slider("Minimum Carrier Occurrences", min_value=2, max_value=20, value=3)
    pmi_df = engine.compute_carrier_excess_specificity(min_occurrences=min_occ)
    if not pmi_df.empty:
        fig, ax = plt.subplots(figsize=(8, max(4, len(pmi_df) * 0.35)))
        sns.heatmap(pmi_df, annot=True, fmt=".2f", cmap="vlag", center=0, cbar=True, ax=ax)
        ax.set_title("Carrier-to-Section PMI")
        st.pyplot(fig)
        plt.close(fig)
    else:
        st.warning("Not enough carrier occurrences to compute PMI. Add more folios to your corpus.")

# -----------------------------------------------------------------------------
# 5. Successor Routing (A4)
# -----------------------------------------------------------------------------
elif view_mode == "Successor Routing (A4)":
    st.subheader("A4 Successor Routing: P(Next Control Header | Exit Port)")
    st.markdown("Verifies whether `-al` and `-ar` route transitions into different downstream control headers.")
    routing_df = engine.audit_successor_routing()
    if not routing_df.empty:
        fig, ax = plt.subplots(figsize=(6, 3.5))
        sns.heatmap(routing_df, annot=True, fmt=".3f", cmap="Blues", cbar=True, ax=ax)
        st.pyplot(fig)
        plt.close(fig)
    else:
        st.warning("Insufficient sequential transitions available to calculate routing.")

# -----------------------------------------------------------------------------
# 6. Token Decomposition Matrix
# -----------------------------------------------------------------------------
elif view_mode == "Token Decomposition Matrix":
    st.subheader("Corpus Token Decomposition Table")
    display_cols = [
        "folio", "section", "currier", "clean", "control", 
        "carrier_core", "e_grade", "exit_port", "state", "is_line_end"
    ]
    st.dataframe(df[display_cols].head(200), use_container_width=True)
