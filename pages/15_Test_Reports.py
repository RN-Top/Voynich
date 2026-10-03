"""
STREAMLIT PAGE: TEST REPORTS
The reports of every pre-registered test, exactly as they were run (from output/).
"""

from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "output"

st.set_page_config(page_title="Test Reports", page_icon="📋", layout="wide")
st.title("📋 Test Reports")
st.markdown("""
Every test below had its rules written down and committed **before** it was first run (the pre-registrations are in
`analyses/*_prereg.md`). These are the reports from those runs, unedited except for notes added afterwards, which are
labelled as such. The short summary is in **FINDINGS.md**, and the full ledger of passes and failures is in
**VALIDATION.md**.
""")

REPORTS = {
    "Held up": [
        ("Plant-page openings ↔ star labels", "plant_star_report.md"),
        ("Map of name links between sections", "name_map_report.md"),
        ("Root dictionary (word cores by section)", "root_dictionary_report.md"),
        ("Rare symbols in first lines", "rare_symbols_report.md"),
        ("Writing types, word order, topic", "writing_types_report.md"),
        ("Set phrases and grammar links", "phrases_report.md"),
        ("Refrains (3- and 4-word repeats)", "refrains_report.md"),
    ],
    "Did not hold up": [
        ('"o" as a name-forming prefix', "o_prefix_report.md"),
        ("Fibonacci numbers", "fibonacci_report.md"),
        ("Bath roots in bath-picture labels", "bath_roots_report.md"),
        ("Labels in their own page's text (ground test)", "ground_report.md"),
        ("Pharmacy labels as plant names", "plant_anchor_report.md"),
        ("Label beginnings vs picture kind", "dictionary_report.md"),
        ("Zodiac halves", "zodiac_halves_report.md"),
        ("Alchemy", "alchemy_report.md"),
        ("Measuring instrument", "instrument_report.md"),
        ("Fifth element in the cycle", "fifth_element_report.md"),
    ],
}

group = st.radio("Show", list(REPORTS), horizontal=True)
options = [(t, f) for t, f in REPORTS[group] if (OUT / f).exists()]
title = st.selectbox("Report", [t for t, _ in options])
fname = dict(options)[title]
st.caption(f"Source: `output/{fname}`")
st.markdown((OUT / fname).read_text(encoding="utf-8"))
