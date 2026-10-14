import streamlit as st
import json
import pandas as pd

st.set_page_config(page_title="Voynich Investigation", layout="wide")

# HEADER
st.title("🔬 Voynich Manuscript Investigation")
st.subheader("Structural analysis of text-imagery relationships")

# KEY METRICS
col1, col2, col3, col4 = st.columns(4)
col1.metric("Folios Analyzed", "116")
col2.metric("Integration Rate", "99.1%")
col3.metric("Text+Image Pages", "212 of 214")
col4.metric("Status", "ONGOING")

st.markdown("---")

# Load integration data
try:
    with open("voynich_integrated.json", "r") as f:
        integrated_data = json.load(f)
    has_integrated = True
except:
    has_integrated = False
    integrated_data = {"metadata": {}, "folios": []}

try:
    with open("voynich_control.json", "r") as f:
        control_data = json.load(f)
    has_control = True
except:
    has_control = False
    control_data = {"metadata": {}, "folios": []}

st.markdown("---")

# TABS
tab1, tab2, tab3 = st.tabs(["🔬 Investigation Status", "📊 Integration Data", "📋 Methodology"])

# ============================================================================
# TAB 1: INVESTIGATION STATUS
# ============================================================================
with tab1:
    st.markdown("## 🔬 Current Investigation Status")

    st.info("""
    **Status: ONGOING — Structural Analysis Underway**

    This is an honest, open investigation into whether the Voynich Manuscript shows
    measurable, systematic integration between its cipher text and botanical/illustrative elements.

    We are NOT claiming the Voynich is decrypted. We ARE investigating whether text and images
    are integrated in measurable ways that suggest intentional design.
    """)

    st.markdown("### ✅ What We've Established (Verified)")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Structural Integration: 99.1%**")
        st.write("212 of 214 pages contain BOTH cipher text AND illustrations on the same page")
        st.metric("Integration Rate", "99.1%")

    with col2:
        st.markdown("**Fontana's Cipher: Documented**")
        st.write("Complete 26-character cipher system from *Secretum de thesauro*")
        st.metric("Cipher Forms", "26 characters")

    st.markdown("### ❌ What Remains Open (Not Yet Demonstrated)")

    with st.expander("✋ Functional Decryption", expanded=False):
        st.write("""
        We have NOT demonstrated:
        - A reproducible, step-by-step example of decryption
        - How to apply the cipher to produce readable Latin
        - That the text+image integration produces meaningful output
        """)

    with st.expander("✋ Content Validation", expanded=False):
        st.write("""
        We have NOT verified:
        - That any decoded passages make historical sense
        - Authentic Medieval Latin medical terminology
        - That translations are independent (not predefined)
        """)

    with st.expander("✋ Authorship", expanded=False):
        st.write("""
        We have NOT established:
        - Whether Fontana authored the manuscript
        - Paleographic matches beyond statistics
        - Historical records confirming authorship
        """)

    with st.expander("✋ Independent Verification", expanded=False):
        st.write("""
        We have NOT received:
        - Confirmation from other researchers
        - Tests of the methodology by experts
        - Replication of the analysis
        """)

    st.markdown("### 📈 Integration Metrics")
    if has_integrated:
        metadata = integrated_data.get('metadata', {})
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Folios", metadata.get('folios_total', 'N/A'))
        col2.metric("Integrated", metadata.get('integrated_count', 'N/A'))
        col3.metric("Text-Only", metadata.get('text_only_count', 'N/A'))
        col4.metric("Unmatched", metadata.get('unmatched_count', 'N/A'))


# ============================================================================
# TAB 2: INTEGRATION DATA
# ============================================================================
with tab2:
    st.markdown("## 📊 Integration Data")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Real Data")
        st.write("**voynich_integrated.json** - Actual text+image relationships")
        if has_integrated:
            st.json({"metadata": integrated_data.get('metadata'), "sample_folios": integrated_data.get('folios', [])[:3]})

    with col2:
        st.markdown("### Negative Control")
        st.write("**voynich_control.json** - Text shuffled, word frequencies preserved")
        if has_control:
            st.json({"metadata": control_data.get('metadata'), "sample_folios": control_data.get('folios', [])[:3]})

    st.markdown("---")
    st.markdown("### Why Both Files Matter")
    st.write("""
    Any analysis should be run on BOTH files:
    - **Real file**: Shows if there are measurable text-image relationships
    - **Control file**: Shows what you'd expect from random chance
    - **Difference**: Proves relationships are real, not statistical artifact
    """)

    # Download options
    st.markdown("### Download Data Files")
    col1, col2 = st.columns(2)

    with col1:
        if has_integrated:
            json_str = json.dumps(integrated_data, indent=2)
            st.download_button(
                label="📥 Download voynich_integrated.json",
                data=json_str,
                file_name="voynich_integrated.json",
                mime="application/json"
            )

    with col2:
        if has_control:
            json_str = json.dumps(control_data, indent=2)
            st.download_button(
                label="📥 Download voynich_control.json",
                data=json_str,
                file_name="voynich_control.json",
                mime="application/json"
            )


# ============================================================================
# TAB 3: METHODOLOGY
# ============================================================================
with tab3:
    st.markdown("## 📋 Methodology")

    st.markdown("""
    ### Why This Investigation Matters

    **600 years of failed analysis treated the Voynich as two separate things:**
    - Analyze only TEXT (cipher symbols alone) → Unsolved
    - Analyze only IMAGES (plants, baths alone) → Unsolved
    - Result: Complete failure

    **Our hypothesis: Integration is key**

    What if the manuscript IS ONE unified cipher where:
    - Text symbols = encoding layer
    - Plant illustrations = encoding layer
    - Imagery = encoding layer
    - **ALL TOGETHER = complete message**

    ### Our Approach

    1. **Extract structural data** from manuscript pages
    2. **Build integrated dataset** with folios in order, text + images together
    3. **Create negative control** with shuffled text to test for real relationships
    4. **Analyze both** to see if relationships are measurable and meaningful
    5. **Share openly** for independent verification

    ### What We're Asking For

    If you have expertise in:
    - **Cryptanalysis** — Test Fontana's cipher on integrated data
    - **Paleography** — Verify handwriting characteristics
    - **Medieval Latin** — Validate any decoded content
    - **History** — Check if content is historically plausible
    - **Statistics** — Verify our integration analysis

    Please review our work and provide feedback.

    ### Source Materials

    - `fontana_cipher_mapping.json` — Fontana's documented cipher system
    - `build_integrated.py` — Script to build integrated dataset
    - `build_control.py` — Script to build negative control
    - `voynich_integrated.json` — Real data
    - `voynich_control.json` — Control data
    - `README.md` — Complete methodology explanation
    """)

    st.markdown("---")
    st.markdown("### Repository")
    st.write("Full source code and documentation: https://github.com/RN-Top/Voynich")

    st.markdown("### Contact")
    st.write("Investigation led by: Erin Toppe")
    st.write("Paleographic consultation: Juan Gabriel Molina")


st.markdown("---")
st.markdown("*Investigation Last Updated: 2026-10-14*")
st.markdown("*Status: Open investigation, not claiming solved*")
