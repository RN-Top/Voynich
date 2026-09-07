"""
voynich-state-viewer: Interactive Astronomical Decipherment Workbench
Connects factorized token morphology directly to 15th-century celestial diagrams.
"""

import os
import io
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

from parser import VoynichMorphology, parse_zl3b, STATE_COLORS, FOLIO_DOMAIN_MAP
from decoder import ZodiacDeciphermentOracle

st.set_page_config(
    page_title="Voynich Astronomical Decipherment Workbench",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

DEFAULT_DATA_PATH = os.path.join("data", "ZL3b-n.txt")


@st.cache_data(show_spinner="Parsing transliteration corpus...")
def load_data():
    if os.path.exists(DEFAULT_DATA_PATH):
        return parse_zl3b(DEFAULT_DATA_PATH)
    return None


st.title("Voynich Astronomical Decipherment Workbench")
st.caption("Cross-Modal Decoding Engine: Aligning Isolated Lexical Carriers (Lambda) to Zodiac Rota Diagrams")

df = load_data()

# Fallback uploader if local data/ZL3b-n.txt is missing
if df is None:
    st.sidebar.warning("`data/ZL3b-n.txt` not found on server.")
    uploaded = st.sidebar.file_uploader("Upload ZL3b-n.txt Corpus", type=["txt"])
    if uploaded is not None:
        temp_path = "temp_corpus.txt"
        with open(temp_path, "wb") as f:
            f.write(uploaded.getvalue())
        df = parse_zl3b(temp_path)
        if os.path.exists(temp_path):
            os.remove(temp_path)
    else:
        st.info("Please supply `ZL3b-n.txt` in the `data/` folder or upload it above to launch.")
        st.stop()

oracle = ZodiacDeciphermentOracle(df)

# Sidebar Controls
st.sidebar.markdown("---")
st.sidebar.header("Decipherment Modes")
mode = st.sidebar.radio(
    "Select Objective",
    [
        "1. Zodiac Sign Alignment",
        "2. Astronomical Carrier PMI",
        "3. Deciphered Zodiac Label Stream",
        "4. Folio Visual Inspection"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown(f"**Total Tokens:** {len(df):,}")
astro_count = df["is_astro"].sum()
st.sidebar.markdown(f"**Astro Tokens:** {astro_count:,} ({astro_count/len(df)*100:.1f}%)")

# =============================================================================
# MODE 1: Zodiac Sign Alignment
# =============================================================================
if mode == "1. Zodiac Sign Alignment":
    st.subheader("Carrier Core Alignment Across the 12 Zodiac Houses")
    st.markdown(
        "By holding the external celestial referent constant (Aries, Taurus, Cancer, etc.), "
        "we can test which **lexical carriers ($\Lambda$)** function as invariant astronomical substantives "
        "versus variable operational syntax."
    )
    
    freq_thresh = st.slider("Minimum Carrier Occurrences in Zodiac", min_value=2, max_value=15, value=3)
    z_matrix = oracle.get_zodiac_carrier_matrix(min_freq=freq_thresh)

    if not z_matrix.empty:
        fig, ax = plt.subplots(figsize=(10, max(4, len(z_matrix) * 0.4)))
        sns.heatmap(z_matrix, annot=True, fmt="d", cmap="YlGnBu", cbar=True, ax=ax, linewidths=0.5)
        ax.set_title("Carrier Occurrences across Canonical Zodiac Folios")
        ax.set_xlabel("Zodiac House (Target Astronomical Prior)")
        ax.set_ylabel("Normalized Carrier Core (Lambda)")
        st.pyplot(fig)
        plt.close(fig)

        st.markdown("#### Carrier Distribution Data")
        st.dataframe(z_matrix, use_container_width=True)
    else:
        st.warning("No carriers met the frequency threshold in the currently loaded zodiac folios.")

# =============================================================================
# MODE 2: Astronomical Carrier PMI
# =============================================================================
elif mode == "2. Astronomical Carrier PMI":
    st.subheader("Pointwise Mutual Information: Carrier Specificity in Celestial Sections")
    st.markdown(
        "Carriers with **PMI > 1.0** represent vocabulary strictly constrained to astronomical diagrams "
        "and circular rotas, proving non-random domain specificity without projecting subjective translations."
    )
    pmi_df = oracle.compute_carrier_astronomical_specificity()
    if not pmi_df.empty:
        col1, col2 = st.columns([1.5, 1])
        with col1:
            fig, ax = plt.subplots(figsize=(6, 8))
            top_pmi = pmi_df.head(25)
            sns.barplot(x="Astronomical", y=top_pmi.index, data=top_pmi, palette="mako", ax=ax)
            ax.set_xlabel("PMI (Astronomical Section Specificity)")
            ax.set_ylabel("Carrier Core (Lambda)")
            st.pyplot(fig)
            plt.close(fig)
        with col2:
            st.write("#### Top Specific Carriers")
            st.dataframe(pmi_df.head(30), use_container_width=True)

# =============================================================================
# MODE 3: Deciphered Zodiac Label Stream
# =============================================================================
elif mode == "3. Deciphered Zodiac Label Stream":
    st.subheader("Targeted Astronomical Carrier Decoding Stream")
    st.markdown(
        "Isolated instances of the core celestial candidates (`OTCHEOD`, `OEEOD`, `OPAIR`, `OTEOD`) "
        "mapped with their realization ports ($\rho$) and angular clock positions on the circular vellum rotas."
    )
    decoded_labels = oracle.decode_zodiac_labels()
    if not decoded_labels.empty:
        st.dataframe(decoded_labels, use_container_width=True)
    else:
        st.info("No targeted astronomical carriers detected in the parsed zodiac records.")

# =============================================================================
# MODE 4: Folio Visual Inspection
# =============================================================================
elif mode == "4. Folio Visual Inspection":
    folios = sorted(df["folio"].unique())
    selected_folio = st.selectbox("Choose Folio", folios, index=folios.index("f72r3") if "f72r3" in folios else 0)
    sub = df[df["folio"] == selected_folio]

    st.markdown(f"**Folio:** `{selected_folio}` | **Zodiac Target:** `{sub['zodiac_sign'].iloc[0]}` | **Currier Hand:** `{sub['currier'].iloc[0]}`")

    # Render HTML spans
    html_out = ['<div style="font-family:monospace; line-height:2.2; font-size:14px; padding:14px; background:#181818; border-radius:8px;">']
    current_line = None
    for _, row in sub.iterrows():
        if row["header"] != current_line:
            if current_line is not None:
                html_out.append("<br/>")
            current_line = row["header"]
            clock_info = f" ({row['clock_pos']})" if row["clock_pos"] != "UNKNOWN" else ""
            html_out.append(f'<span style="color:#777; font-size:11px;">[{row["header"]}{clock_info}] </span>')

        color = STATE_COLORS.get(row["state"], "#9E9E9E")
        html_out.append(
            f'<span style="background-color:{color}; color:#000; padding:2px 5px; margin:2px; '
            f'border-radius:3px; font-weight:bold;" title="Carrier: {row["carrier"]} | Port: {row["exit_port"]}">'
            f'{row["clean"]}</span> '
        )
    html_out.append('</div>')
    st.markdown("".join(html_out), unsafe_allow_html=True)
