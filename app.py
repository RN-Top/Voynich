"""
VOYNICH UNIFIED DECIPHERMENT ENGINE & PHONETIC CONSOLE
Consolidates:
1. Thematic Technical Load vs. Universal Syntactic Backbone (Chi-Square & PMI).
2. Ptolemaic Decan Radial Grounding & Sukhotin Vowel/Consonant Partition.
3. Live Interactive Phonetic Reading Console for continuous line translation.
"""

import math
import re
import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Voynich Unified Decipherment Suite",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🌌 Voynich Unified Decipherment Suite")
st.caption("Consolidating Thematic Contingency, Ptolemaic Decan Grounding, and Continuous Line Translation.")

# -----------------------------------------------------------------------------
# 1. PHONETIC ENGINE & HISTORICAL TARGETS
# -----------------------------------------------------------------------------
SUKHOTIN_VOWELS = set(['a', 'o', 'h', 't', 'i', 'y'])
SUKHOTIN_CONSONANTS = set(['c', 'd', 'e', 'f', 'k', 'l', 'm', 'n', 'p', 's', 'r'])

PHONETIC_ALPHABET = {
    'o': 'o', 't': 't', 'c': 's', 'h': 'a', 'e': 'r', 'd': 'n',
    'a': 'u', 'i': 'i', 'q': 'c', 'k': 'o', 'p': 'm', 'm': 's',
    'y': 'm', 's': 'p', 'l': 'l', 'r': 'r', 'f': 'f'
}

HISTORICAL_DECANS = [
    {"sign": "Pisces (f70v2)", "decan": 1, "target": "PASIS", "target_cv": "CVCVC", "ruler": "SATURNUS", "ruler_cv": "CVCVCCVC"},
    {"sign": "Pisces (f70v2)", "decan": 2, "target": "ARAT", "target_cv": "VCVC", "ruler": "JUPITER", "ruler_cv": "CVCVCVC"},
    {"sign": "Pisces (f70v2)", "decan": 3, "target": "FLAC", "target_cv": "CCVC", "ruler": "MARS", "ruler_cv": "CVCC"},
    {"sign": "Aries (f71r)", "decan": 1, "target": "ASCLIR", "target_cv": "VCCCVC", "ruler": "MARS", "ruler_cv": "CVCC"},
    {"sign": "Aries (f71r)", "decan": 2, "target": "CALCOT", "target_cv": "CVCCVC", "ruler": "SOL", "ruler_cv": "CVC"},
    {"sign": "Aries (f71r)", "decan": 3, "target": "AROB", "target_cv": "VCVC", "ruler": "VENUS", "ruler_cv": "CVCVC"},
    {"sign": "Taurus (f72r1)", "decan": 1, "target": "KOCAR", "target_cv": "CVCVC", "ruler": "MERCURIUS", "ruler_cv": "CVCCVCVVC"},
    {"sign": "Taurus (f72r1)", "decan": 2, "target": "MAHAR", "target_cv": "CVCVC", "ruler": "LUNA", "ruler_cv": "CVCV"},
    {"sign": "Taurus (f72r1)", "decan": 3, "target": "SARAM", "target_cv": "CVCVC", "ruler": "SATURNUS", "ruler_cv": "CVCVCCVC"}
]

RADIAL_SPOKES = [
    {"folio": "f70v2", "label": "otcheod", "sign": "Pisces (f70v2)"},
    {"folio": "f70v2", "label": "oteodal", "sign": "Pisces (f70v2)"},
    {"folio": "f71r", "label": "opairam", "sign": "Aries (f71r)"},
    {"folio": "f71r", "label": "okeal", "sign": "Aries (f71r)"},
    {"folio": "f72r1", "label": "otcheor", "sign": "Taurus (f72r1)"},
    {"folio": "f72r1", "label": "dal", "sign": "Taurus (f72r1)"}
]

def clean_stem(token: str) -> str:
    w = re.sub(r"[{}\[\]<!>]", "", str(token).lower().strip())
    w = re.sub(r"^(qk|dk|qok|qot|qop|qo|ok|ot|op|da|ch|sh)", "", w)
    w = re.sub(r"(aiiin|aiin|ain|eedy|edy|eey|ey|al|ar|am|or|ol|m|y)$", "", w)
    return w if w else token

def get_voynich_cv(word: str) -> str:
    skel = []
    for c in str(word).lower():
        if c in SUKHOTIN_VOWELS:
            skel.append("V")
        elif c in SUKHOTIN_CONSONANTS:
            skel.append("C")
    return "".join(skel)

def levenshtein_ratio(s1: str, s2: str) -> float:
    if s1 == s2:
        return 1.0
    l1, l2 = len(s1), len(s2)
    dp = [[0] * (l2 + 1) for _ in range(l1 + 1)]
    for i in range(l1 + 1): dp[i][0] = i
    for j in range(l2 + 1): dp[0][j] = j
    for i in range(1, l1 + 1):
        for j in range(1, l2 + 1):
            cost = 0 if s1[i - 1] == s2[j - 1] else 1
            dp[i][j] = min(dp[i - 1][j] + 1, dp[i][j - 1] + 1, dp[i - 1][j - 1] + cost)
    max_len = max(l1, l2)
    return round(1.0 - (dp[l1][l2] / max_len), 3) if max_len else 0.0

def decode_phonetic(line: str) -> str:
    words = line.split()
    decoded = []
    for w in words:
        cleaned = re.sub(r"[^a-z]", "", w.lower())
        decoded.append("".join(PHONETIC_ALPHABET.get(c, c) for c in cleaned))
    return " ".join(decoded)

# -----------------------------------------------------------------------------
# 2. CONTINGENCY & MUTUAL INFORMATION MATRICES
# -----------------------------------------------------------------------------
SECTIONS = ["Herbal", "Biological", "Astronomical", "Recipes"]
CARRIERS = ["ch", "t", "ot", "ok", "ol", "shed"]

RAW_COUNTS = np.array([
    [3480, 1380, 720, 911],  # ch
    [815,   265, 163, 237],  # t
    [552,   541, 402, 164],  # ot
    [346,   618,  55, 100],  # ok
    [174,   429,  36, 111],  # ol
    [53,    285,  12,  18],  # shed
], dtype=float)

row_totals = RAW_COUNTS.sum(axis=1)
col_totals = RAW_COUNTS.sum(axis=0)
grand_total = RAW_COUNTS.sum()

expected = np.outer(row_totals, col_totals) / grand_total
std_residuals = (RAW_COUNTS - expected) / np.sqrt(expected)

p_joint = RAW_COUNTS / grand_total
p_carrier = row_totals / grand_total
p_section = col_totals / grand_total
pmi = np.zeros_like(RAW_COUNTS)
for i in range(len(CARRIERS)):
    for j in range(len(SECTIONS)):
        pmi[i, j] = math.log2(p_joint[i, j] / (p_carrier[i] * p_section[j]))

chi2_stat = np.sum((RAW_COUNTS - expected) ** 2 / expected)
degrees_of_freedom = (len(CARRIERS) - 1) * (len(SECTIONS) - 1)

# -----------------------------------------------------------------------------
# 3. INTERFACE TABS
# -----------------------------------------------------------------------------
t1, t2, t3, t4 = st.tabs([
    "🧪 1. Live Phonetic Line Reader",
    "🎯 2. Decan Skeletal Anchors",
    "📊 3. Thematic Contingency & Z-Scores",
    "🧮 4. Pointwise Mutual Information"
])

with t1:
    st.subheader("Holdout Phonetic & Syllabic Reading Console")
    st.markdown("Decode continuous lines using the candidate phonetic alphabet derived from Ptolemaic decans and Sukhotin partitions.")
    
    preset_lines = {
        "Folio f114v.21 (Stars / Recipe Holdout)": "otcheodaiin qokchdy otedal dain aral qokedy",
        "Folio f1r.1 (Herbal Opening Title)": "fachys ykal ar ataiin shol shory cthores y kor sholdy",
        "Folio f70v2 (Pisces Decan Spoke String)": "otcheod oteodal opairam okeal otcheor dal",
        "Custom Entry": ""
    }
    choice = st.selectbox("Select Preset Folio Line:", list(preset_lines.keys()))
    if choice == "Custom Entry":
        user_line = st.text_input("Enter Voynich line (EVA):", "qokedy otcheodaiin qopairam otcheody daiin chedy")
    else:
        user_line = preset_lines[choice]

    c_a, c_b = st.columns(2)
    with c_a:
        st.markdown("**Transliterated Cipher Input:**")
        st.code(user_line, language="text")
        st.markdown("**Decoded Phonetic Plaintext:**")
        st.code(decode_phonetic(user_line), language="text")
    with c_b:
        st.markdown("**Consonant-Vowel (CV) Skeleton:**")
        st.code(" ".join(get_voynich_cv(w) for w in user_line.split()), language="text")
        st.markdown("**Phonetic Key Mapping:**")
        st.dataframe(pd.DataFrame([{"Glyph": k, "Sound": v.upper()} for k, v in PHONETIC_ALPHABET.items()]).T, use_container_width=True)

with t2:
    st.subheader("Ptolemaic Decan Consonant-Vowel Alignment")
    rows = []
    for spoke in RADIAL_SPOKES:
        carrier = clean_stem(spoke["label"])
        v_cv = get_voynich_cv(carrier)
        match = [d for d in HISTORICAL_DECANS if d["sign"] == spoke["sign"]][0]
        s_decan = levenshtein_ratio(v_cv, match["target_cv"]) * 100.0
        s_ruler = levenshtein_ratio(v_cv, match["ruler_cv"]) * 100.0
        rows.append({
            "Folio": spoke["folio"],
            "Radial Label": spoke["label"],
            "Carrier Stem": carrier,
            "Voynich CV": v_cv,
            "Target Decan": match["target"],
            "Decan CV": match["target_cv"],
            "Decan Fit": f"{s_decan:.1f}%",
            "Planetary Ruler": match["ruler"],
            "Ruler CV": match["ruler_cv"],
            "Ruler Fit": f"{s_ruler:.1f}%",
            "Verdict": "HIGH MATCH" if max(s_decan, s_ruler) >= 70.0 else "PARTIAL"
        })
    st.dataframe(pd.DataFrame(rows), use_container_width=True)

with t3:
    st.subheader("Thematic Contingency & Standardized Residuals")
    st.markdown(f"**Chi-Square Independence:** $\\chi^2 = {chi2_stat:.2f}$ ($df = {degrees_of_freedom}, p < 10^{{-50}}$)")
    st.dataframe(pd.DataFrame(std_residuals, index=CARRIERS, columns=SECTIONS).round(2), use_container_width=True)

with t4:
    st.subheader("Pointwise Mutual Information (PMI in Bits)")
    st.dataframe(pd.DataFrame(pmi, index=CARRIERS, columns=SECTIONS).round(3), use_container_width=True)
