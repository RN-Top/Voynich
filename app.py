"""
THE RHAZES ORIGIN INVESTIGATION

Research proving a 9th-century Persian physician's framework
spread across medieval Europe, appearing in both Fermoy and Voynich manuscripts.

Investigation: Erin Toppe
Methodology: Framework analysis, manuscript comparison, archival research
Repository: github.com/RN-Top/Voynich

Live on Streamlit Cloud: https://voynich.streamlit.app
"""

import streamlit as st

st.set_page_config(
    page_title="Rhazes Origin Investigation",
    page_icon="📜",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================================
# CENTRAL QUESTION
# ============================================================================

st.title("🔍 The Origin Investigation")
st.markdown("""
### The Central Question

**Where did the systematic framework in Fermoy and Voynich manuscripts come from?**

### What We Know

A framework appears in THREE places:
- **Rhazes' texts** (9th century, Baghdad): Condition → Cause → Cure
- **Fermoy manuscript** (~1400, Ireland): Identical framework (75% match)
- **Voynich manuscript** (~1404-1438, unknown): Identical framework (100% structured)

### What We DON'T Know

- ✗ Did Rhazes **originate** this framework?
- ✗ Or did he **systematize** an older medical tradition?
- ✗ What were his sources? Who trained him?
- ✗ Why did HIS systematization become the medieval standard (not others')?
- ✗ How exactly did it reach Ireland and Voynich?

### How We're Investigating

**We're tracing BACKWARD and FORWARD:**
1. **BACKWARD** - What came before Rhazes? Was he the originator or systematizer?
2. **UNDERSTAND** - Why did his approach become standard? What made him different?
3. **FORWARD** - How did his work spread? How did it reach Fermoy and Voynich?

**This is honest investigation. No predetermined answer. Follow the evidence.**
""")

st.markdown("---")

# ============================================================================
# CORE EVIDENCE
# ============================================================================

st.markdown("## 📊 What We Have")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Rhazes Texts",
        "7 Digitized",
        "Framework: YES"
    )

with col2:
    st.metric(
        "Fermoy",
        "75% Match",
        "Condition→Cause→Cure"
    )

with col3:
    st.metric(
        "Voynich",
        "100% Structured",
        "Same framework"
    )

with col4:
    st.metric(
        "The Question",
        "UNKNOWN",
        "Origin or systematizer?"
    )

st.markdown("""
### The Framework Pattern

**Same organizational logic in all three:**
1. **Rhazes' texts** - Condition → Cause → Cure framework present
2. **Fermoy manuscript** - Irish adaptation, 75% framework match
3. **Voynich manuscript** - Cipher adaptation, 100% structured

**Identical framework. Different languages. Different scripts.**

### The Investigation

This pattern suggests they come from a common source. But **WHO is that source?**
- Was it Rhazes (originator)?
- Was it someone before Rhazes (who he systematized)?
- Was it a gradual evolution Rhazes formalized?

**We don't know yet. That's what we're investigating.**

See: INVESTIGATION_STRUCTURE.md for the three investigation paths (Backward, Rhazes, Forward)
""")

st.markdown("---")

# ============================================================================
# CURRENT RESEARCH
# ============================================================================

st.markdown("## 🔬 Current Supporting Tests")

st.markdown("""
## Testing & Results

### What We Confirmed:
1. **Voynich-Fermoy Vocabulary Connection** — 28,185 Levenshtein matches exist
   ✓ THIS IS REAL

2. **Section-Specific Matching** — Voynich matches different Fermoy sections with 67% variation
   ✓ NOT RANDOM (some sections match 1.67x better than others)

3. **Genealogical Evidence** — Ó hÍceadha name in Fermoy margins (Todd catalogue)
   ✓ DOCUMENTED FACT

4. **Structural Pattern** — Symptoms → Causes → Cures framework exists in both texts
   ✓ VERIFIABLE

5. **Closing Vocabulary Test** — 44 formulaic words at 2–3× chance rate
   ✓ SUPPORTED (p < 0.05)

6. **Bathing Season Pattern** — Spring figures in tubs 74% vs 1% other seasons
   ✓ SUPPORTED (p < 0.001)

### What We Tested & It Failed:
**❌ Medical Vocabulary Hypothesis — REJECTED**

Original claim: "Medical vocabulary is the connection between Voynich and Fermoy"

Test result: Medical vocabulary matches WORSE than non-medical Fermoy text (0.82x ratio)

Why it failed:
- Original vocabulary included common words ("begins," "hand," "king," "old")
- After filtering contaminants, signal disappeared
- Control group (non-medical Fermoy) matched equally well or better
- Conclusion: Connection is NOT medical-vocabulary-specific

This is honest science. We tested it. It failed. We're correcting course.
""")

st.markdown("---")

st.markdown("## ✓ Test Results That Confirm This")

st.markdown("""
**All tests were pre-registered BEFORE analysis.**
All methodology, code, and results are reproducible and in the public GitHub repository.

### Supporting Tests:
- **Fermoy Vocabulary Comparison Test** — 66 Levenshtein + 32 substring matches (p < 0.05)
- **Section-by-Section Vocabulary Test** — Complete analysis across all 6 Voynich sections
- **Structural Match Test** — Voynich follows identical medical format (Symptoms → Causes → Cures)
- **Closing Vocabulary Test** — 44 formulaic words at 2-3× chance rate
- **Bathing Season Pattern** — Spring 74% vs 1% other seasons (p < 0.001)

### Full Reproducibility:
Every test has:
- Pre-registration document (written before running)
- Source code (in `analyses/` directory)
- Test report (in `output/` directory)
- Data files (in `data/` directory)

**You can reproduce every result yourself.**
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
