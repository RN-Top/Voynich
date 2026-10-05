"""
EXPLORATORY ARCHIVE: Historical Tests

This section contains 50+ tests from the early exploratory phase of research.
These were rigorous pre-registered hypothesis tests that did NOT support their hypotheses,
which is valuable information. They are archived here to keep the main research focused.
"""

import streamlit as st
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "output"

st.set_page_config(page_title="Exploratory Archive", page_icon="🗂️", layout="wide")

st.title("🗂️ Exploratory Archive")

st.markdown("""
These 50+ tests were important for understanding what the Voynich **is not**.
They were rigorous, pre-registered, and carefully executed. The fact that they did
not support their hypotheses is scientifically valuable.

They are archived here to keep the main research focused on what **does** work.

See the full ledger in **VALIDATION.md** in the repository.
""")

st.markdown("---")

# Old exploratory tests
ARCHIVE_REPORTS = {
    "Linguistic & Grammar Tests": [
        ("Writing types, word order, topic", "writing_types_report.md"),
        ("Set phrases and grammar links", "phrases_report.md"),
        ("Refrains (3- and 4-word repeats)", "refrains_report.md"),
        ("Scribe vs topic; rules hold for every scribe", "scribes_report.md"),
        ("Shared grammar table across scribes", "grammar_table_report.md"),
        ("Vowels and consonants (Sukhotin)", "vowels_report.md"),
    ],
    "Structural & Spatial Tests": [
        ("Plant-page openings ↔ star labels", "plant_star_report.md"),
        ("Map of name links between sections", "name_map_report.md"),
        ("Root dictionary (word cores by section)", "root_dictionary_report.md"),
        ("Rare symbols in first lines", "rare_symbols_report.md"),
        ("Diagram labels as measurements (weak)", "coordinates_report.md"),
        ("Measurement or writing drift? (position)", "coord_vs_drift_report.md"),
        ("Writing orientation ruled out", "orientation_report.md"),
    ],
    "Astronomical & Numerical Tests": [
        ("Fibonacci numbers", "fibonacci_report.md"),
        ("Sun–Moon phase pages", "sun_moon_report.md"),
        ("Zodiac halves", "zodiac_halves_report.md"),
        ("Counting: labels lengthen around wheels?", "counting_report.md"),
    ],
    "Semantic & Content Tests": [
        ('\"o\" as a name-forming prefix', "o_prefix_report.md"),
        ("Bath roots in bath-picture labels", "bath_roots_report.md"),
        ("Labels in their own page's text (ground test)", "ground_report.md"),
        ("Pharmacy labels as plant names", "plant_anchor_report.md"),
        ("Label beginnings vs picture kind", "dictionary_report.md"),
        ("Fifth element in the cycle", "fifth_element_report.md"),
    ],
    "Specialized Tests": [
        ("Alchemy", "alchemy_report.md"),
        ("Measuring instrument", "instrument_report.md"),
        ("Glue words and grammar", "glue_words_report.md"),
        ("Anomaly scan", "anomaly_scan_report.md"),
    ],
}

for category, reports in ARCHIVE_REPORTS.items():
    st.markdown(f"### {category}")
    for name, filename in reports:
        file_path = OUT / filename
        if file_path.exists():
            with open(file_path) as f:
                content = f.read()
            with st.expander(f"📄 {name}"):
                st.markdown(content)
        else:
            st.caption(f"📄 {name} — [report file not found]")
    st.markdown("")

st.markdown("---")

st.markdown("""
### Why Archive These?

These tests were scientifically sound but did not support their hypotheses.
In rigorous research, null results are just as important as positive ones—they
tell us what the manuscript is **not**.

By archiving them separately, we keep the main research focused on what **does**
support the O'Hickey hypothesis while preserving the full historical record of
investigation.

**Every test was pre-registered and unedited.** You can verify the methodology and
results for yourself in the repository.
""")
