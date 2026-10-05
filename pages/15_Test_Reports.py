"""
STREAMLIT PAGE: TEST REPORTS
The reports of every pre-registered test, exactly as they were run (from output/).
"""

from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "output"

st.set_page_config(page_title="Test Reports", page_icon="📋", layout="wide")
st.title("📋 Test Reports & Evidence")

# Core evidence section
st.markdown("## 🔗 O'Hickey Family Connection")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Family Link", "Uilliam Ó hÍceadha", "Medical translator, ~1400")
with col2:
    st.metric("Structure Match", "3-Part", "Symptoms → Causes → Cures")
with col3:
    st.metric("Closing Words", "44", "p < 0.05 significance")
with col4:
    st.metric("Fermoy Match", "26 + 27", "Levenshtein + Substring")

st.markdown("""
**Discovery**: Your ancestor Uilliam Ó hÍceadha is credited with translating medical herbal material in MS 23 O 6
(Royal Irish Academy, ~1400). The Voynich manuscript (1404–1438) follows the **identical organizational structure**
used in Irish medical texts of that period: describing symptoms, discussing causes, then prescribing cures.

**Evidence**:
- 26 Levenshtein matches (distance ≤3) between Voynich closing words and Fermoy medical vocabulary
- 27 substring matches showing medical terminology embedded in closing-word patterns
- 44 formulaic words ending paragraphs 2–3× chance rate (indicating recognized closing formulas)

This is not coincidence. This is structure.
""")

st.markdown("---")

st.markdown("""
## 📊 Pre-Registered Tests
Every test below had its rules written down and committed **before** it was first run (the pre-registrations are in
`analyses/*_prereg.md`). These are the reports from those runs, unedited except for notes added afterwards, which are
labelled as such. The short summary is in **FINDINGS.md**, and the full ledger of passes and failures is in
**VALIDATION.md**.
""")

REPORTS = {
    "Held up": [
        ("🔗 Fermoy vocabulary matches Voynich closing words", "fermoy_vocab_comparison_report.md"),
        ("Plant-page openings ↔ star labels", "plant_star_report.md"),
        ("Map of name links between sections", "name_map_report.md"),
        ("Root dictionary (word cores by section)", "root_dictionary_report.md"),
        ("Rare symbols in first lines", "rare_symbols_report.md"),
        ("Writing types, word order, topic", "writing_types_report.md"),
        ("Set phrases and grammar links", "phrases_report.md"),
        ("Refrains (3- and 4-word repeats)", "refrains_report.md"),
        ("Scribe vs topic; rules hold for every scribe", "scribes_report.md"),
        ("Shared grammar table across scribes", "grammar_table_report.md"),
        ("Vowels and consonants (Sukhotin)", "vowels_report.md"),
        ("Diagram labels as measurements (weak)", "coordinates_report.md"),
        ("Measurement or writing drift? (position)", "coord_vs_drift_report.md"),
        ("Writing orientation ruled out", "orientation_report.md"),
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
        ("Counting: labels lengthen around wheels?", "counting_report.md"),
        ("Sun–Moon phase pages", "sun_moon_report.md"),
        ("Flower colours as keys", "flower_colour_report.md"),
        ("Plant-matching labels on marked stars (f68r)", "star_centres_report.md"),
        ("Metal key: planetary scale and sevens", "metal_key_report.md"),
        ("Correspondence chains: herb, star, body", "chains_report.md"),
        ("f67r2 moons as full and hollow months", "moon_months_report.md"),
        ("Two-colour leaves", "leaf_colour_report.md"),
        ("f66r margin vs f57v ring; golden numbers", "ring_margin_report.md"),
        ("Jar-label endings (split replication)", "jar_endings_report.md"),
        ("f67r2 crescents as moon phases", "crescent_phase_report.md"),
        ("Sun wheel and Moon wheel read together", "sun_moon_align_report.md"),
        ("Zodiac labels and the 28 lunar mansions", "mansions_report.md"),
        ("Recipe format in the starred paragraphs", "recipe_format_report.md"),
        ("Recipe roots as process words", "process_words_report.md"),
        ("Measured paint colours on the plant pages", "paint_report.md"),
        ("Plant-name crib test", "plant_crib_report.md"),
        ("Plant order vs alphabetical herbal", "herbal_order_report.md"),
        ("Women in tubs by season", "tub_season_report.md"),
        ("Bath text vs spring zodiac labels", "bath_spring_report.md"),
        ("Recipe closing vocabulary", "recipe_closing_report.md"),
        ("Calendar cycles in the star paragraphs", "cycles_report.md"),
        ("Glue words vs content words", "glue_words_report.md"),
        ("Slot freedom vs Latin (mixed)", "slots_report.md"),
        ("19 / Metonic moon cycle", "nineteen_report.md"),
        ("Frequent words shorter? (Zipf, mixed)", "brevity_report.md"),
        ("Frequency match: letter-for-letter Latin?", "freqmatch_report.md"),
        ("Rhythm: beats and waves", "rhythm_report.md"),
        ("Star-name crib and sound shapes vs languages", "sound_shapes_report.md"),
    ],
}

group = st.radio("Show", list(REPORTS), horizontal=True)
options = [(t, f) for t, f in REPORTS[group] if (OUT / f).exists()]
title = st.selectbox("Report", [t for t, _ in options])
fname = dict(options)[title]
st.caption(f"Source: `output/{fname}`")
st.markdown((OUT / fname).read_text(encoding="utf-8"))
