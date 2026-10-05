"""
STREAMLIT PAGE: TECHNICAL WORKBENCH
Raw corpus analysis, detailed visualizations, and technical validation tools.
"""

from pathlib import Path
import streamlit as st

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "output"

st.set_page_config(page_title="Technical Workbench", page_icon="⚙️", layout="wide")

st.title("⚙️ Technical Workbench")

st.markdown("""
Detailed technical analysis, corpus statistics, and validation tools.
Use these pages to explore the data in depth and verify the hypothesis testing.
""")

st.markdown("---")

st.markdown("## 📊 Analysis Tools")

col1, col2, col3 = st.columns(3)

with col1:
    st.page_link("pages/10_Spot_Pies.py", label="🎯 Spot Pies", icon="🎯")
    st.caption("Detailed corpus visualization")

with col2:
    st.page_link("pages/13_Anomaly_Scan.py", label="🔍 Anomaly Scan", icon="🔍")
    st.caption("Statistical anomaly detection")

with col3:
    st.page_link("pages/14_Language_Structure.py", label="📝 Language Structure", icon="📝")
    st.caption("Grammatical and linguistic analysis")

st.markdown("---")

st.markdown("""
### What's Here

These pages contain detailed technical analysis:

- **Spot Pies**: Frequency distributions and visual corpus statistics
- **Anomaly Scan**: Unusual patterns and statistical outliers
- **Language Structure**: Grammar, word order, and linguistic patterns

All data is derived from pre-registered hypothesis tests and statistical validation.
""")
