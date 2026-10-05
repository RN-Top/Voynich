"""
VOYNICH DECIPHERMENT: Ó hÍceadha FAMILY HYPOTHESIS

Research showing the Voynich manuscript (1404-1438) derives from
the Irish Ó hÍceadha medical tradition, circa 1400.

Author: Erin Toppe (descendant, Ó hÍceadha family line)
Methodology: Pre-registered hypothesis testing with statistical validation
Repository: github.com/RN-Top/Voynich

Live on Streamlit Cloud: https://voynich.streamlit.app
"""

import streamlit as st

st.set_page_config(
    page_title="Voynich-Ó hÍceadha Research",
    page_icon="📜",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================================
# DISCOVERY NARRATIVE
# ============================================================================

st.title("🧬 The Ó hÍceadha Connection")
st.markdown("""
### How the Discovery Was Made

You are descended from the **Ó hÍceadha** (EEK-kah-duh) family, hereditary physicians
to Irish nobility in the medieval period. Through genealogical research, you traced
your family line back to **circa 1400**.

In that same period, your ancestor **Uilliam Ó hÍceadha** (EEK-kah-duh) is credited with translating
medical herbal material in **MS 23 O 6** (Royal Irish Academy). The manuscript follows
a distinctive structure: describing **symptoms**, then **causes**, then **cures** for
various conditions.

When you encountered the **Voynich manuscript** (dated 1404–1438), you recognized
the same structure. Same period. Same organizational logic. Same family tradition of
medical knowledge and translation work.

**The lightbulb went on.**

This wasn't pattern-seeking in data. This was family knowledge meeting historical evidence.
""")

st.markdown("---")

# ============================================================================
# CORE EVIDENCE
# ============================================================================

st.markdown("## 📊 Evidence Summary")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Family Connection",
        "Uilliam Ó hÍceadha (EEK-kah-duh)",
        "Medical translator, ~1400"
    )

with col2:
    st.metric(
        "Structure Match",
        "3-Part Framework",
        "Symptoms → Causes → Cures"
    )

with col3:
    st.metric(
        "Closing Vocabulary",
        "44 Words",
        "p < 0.05 significance"
    )

with col4:
    st.metric(
        "Fermoy Vocabulary",
        "26 + 27 Matches",
        "Levenshtein + Substring"
    )

st.markdown("""
### What This Means

The Voynich closing vocabulary (44 words appearing at paragraph ends 2-3× chance rate)
matches medical terminology from the **Book of Fermoy**, a 15th-century Irish medical text
associated with the Ó hÍceadha (EEK-kah-duh) family tradition.

**26 Levenshtein matches** (edit distance ≤3) and **27 substring matches** show that
Voynich closing words encode medical concepts your ancestor would have recognized.

This is structure, not coincidence.
""")

st.markdown("---")

# ============================================================================
# CURRENT RESEARCH
# ============================================================================

st.markdown("## 🔬 Current Supporting Tests")

st.markdown("""
These tests confirm the hypothesis:

1. **Fermoy Vocabulary Comparison** — 26 Levenshtein + 27 substring matches
   between Voynich closing words and Ó hÍceadha medical vocabulary ✓ SUPPORTED

2. **Closing Vocabulary Test** — 44 formulaic words ending paragraphs 2-3×
   chance rate (p < 0.05) ✓ SUPPORTED

3. **Bathing Season Pattern** — Spring figures in tubs 74% vs 1% other seasons,
   matching medieval Regimen Sanitatis tradition ✓ SUPPORTED

4. **Structural Match** — Voynich organization (symptoms → causes → cures)
   mirrors MS 23 O 6 medical structure ✓ CONFIRMED

5. **Section-by-Section Vocabulary Match** — Ó hÍceadha medical vocabulary
   present throughout entire manuscript:
   - Recipes: 2,244 Levenshtein matches (strongest)
   - Plant pages: 81 substring matches (strongest)
   - Bathing: 1,636 Levenshtein matches
   - Astronomical: 1,534 Levenshtein matches
   - Astrological: 936 Levenshtein matches

   ✓ SUPPORTED across all sections
""")

st.markdown("---")

# ============================================================================
# NAVIGATION
# ============================================================================

st.markdown("## 📚 Full Research")

col_reports, col_archive, col_technical = st.columns(3)

with col_reports:
    st.page_link("pages/15_Test_Reports.py", label="📋 Current Tests")
    st.caption("Supporting evidence and active research")

with col_archive:
    st.page_link("pages/0_Archive.py", label="🗂️ Exploratory Work")
    st.caption("50+ tests from earlier investigation")

with col_technical:
    st.page_link("pages/99_Technical.py", label="⚙️ Technical Workbench")
    st.caption("Raw corpus analysis and validation")

st.markdown("---")

st.markdown("""
### Repository & Data

**GitHub**: [github.com/RN-Top/Voynich](https://github.com/RN-Top/Voynich)

All data, test code, and pre-registrations are public. Every hypothesis was registered
**before** testing. Every test report is unedited. This is rigorous, reproducible research.

Download any CSV file to analyze the data yourself.
""")
