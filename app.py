import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Voynich Decipherment Workbench",
    page_icon="📜",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# -----------------------------------------------------------------------------
# MASTER DATASETS & SYSTEM SPECIFICATIONS
# -----------------------------------------------------------------------------

# 16-Glyph Phonetic & Grammatical Matrix (from Excel export)
PHONETIC_MATRIX_DATA = [
    {"Voynich Glyph": "o", "Phonetic Sound": "O", "Class": "Vowel",     "Affix Role": "Prefix operational"},
    {"Voynich Glyph": "t", "Phonetic Sound": "T", "Class": "Vowel",     "Affix Role": "Connective"},
    {"Voynich Glyph": "c", "Phonetic Sound": "S", "Class": "Consonant", "Affix Role": "Stem core"},
    {"Voynich Glyph": "h", "Phonetic Sound": "A", "Class": "Vowel",     "Affix Role": "Stem nucleus"},
    {"Voynich Glyph": "e", "Phonetic Sound": "R", "Class": "Consonant", "Affix Role": "Stem core"},
    {"Voynich Glyph": "d", "Phonetic Sound": "N", "Class": "Consonant", "Affix Role": "Terminal marker"},
    {"Voynich Glyph": "a", "Phonetic Sound": "U", "Class": "Vowel",     "Affix Role": "Stem nucleus"},
    {"Voynich Glyph": "i", "Phonetic Sound": "I", "Class": "Vowel",     "Affix Role": "Iterative inflection"},
    {"Voynich Glyph": "q", "Phonetic Sound": "C", "Class": "Consonant", "Affix Role": "Prefix procedural"},
    {"Voynich Glyph": "k", "Phonetic Sound": "O", "Class": "Consonant", "Affix Role": "Thermal marker"},
    {"Voynich Glyph": "p", "Phonetic Sound": "M", "Class": "Consonant", "Affix Role": "Stem core"},
    {"Voynich Glyph": "m", "Phonetic Sound": "S", "Class": "Consonant", "Affix Role": "Terminal buffer flush"},
    {"Voynich Glyph": "y", "Phonetic Sound": "M", "Class": "Vowel",     "Affix Role": "Terminal affix"},
    {"Voynich Glyph": "s", "Phonetic Sound": "P", "Class": "Consonant", "Affix Role": "Stem core"},
    {"Voynich Glyph": "l", "Phonetic Sound": "L", "Class": "Consonant", "Affix Role": "Liquid coda"},
    {"Voynich Glyph": "r", "Phonetic Sound": "R", "Class": "Consonant", "Affix Role": "Liquid coda"},
]

# Corpus Macrostate Distribution
MACROSTATES_DATA = [
    {"role": "unmapped", "count": 16433, "percentage": "42.99%"},
    {"role": "heat",     "count": 7594,  "percentage": "19.87%"},
    {"role": "outlet",   "count": 4350,  "percentage": "11.38%"},
    {"role": "medium",   "count": 4190,  "percentage": "10.96%"},
    {"role": "reflux",   "count": 4123,  "percentage": "10.79%"},
    {"role": "drain",    "count": 1021,  "percentage": "2.67%"},
    {"role": "retain",   "count": 512,   "percentage": "1.34%"},
]

# Procedural Execution Frame Ledger
PROCEDURAL_FRAME_DATA = [
    {"role": "medium", "folio": "f1r", "token": "ataiin"},
    {"role": "medium", "folio": "f1r", "token": "chtaiin"},
    {"role": "medium", "folio": "f1r", "token": "ykaiin"},
    {"role": "medium", "folio": "f1r", "token": "daraiin"},
    {"role": "medium", "folio": "f1r", "token": "daiin"},
    {"role": "heat",   "folio": "f1r", "token": "okaiin"},
    {"role": "medium", "folio": "f1r", "token": "cthaiin"},
    {"role": "medium", "folio": "f1r", "token": "cfhaiin"},
    {"role": "medium", "folio": "f1r", "token": "cfhoaiin"},
    {"role": "medium", "folio": "f1r", "token": "daiin"},
]

# Astrological Zodiac Spoke Registry
ZODIAC_SPOKES_DATA = [
    {"folio": "f70v2", "spoke_label": "otcheod", "core_stem": "cheod", "voynich_cv": "CVCVC", "target_candidate": "PASIS (Pisces 330°-360°)"},
    {"folio": "f70v2", "spoke_label": "oteodal", "core_stem": "eodal", "voynich_cv": "CVCVC", "target_candidate": "RADIS (Pisces Decan 2)"},
    {"folio": "f71r",  "spoke_label": "opairam", "core_stem": "pair",  "voynich_cv": "CVVC",  "target_candidate": "ARIES / MAUR (000°-030°)"},
    {"folio": "f71r",  "spoke_label": "okeal",   "core_stem": "keal",  "voynich_cv": "CCVC",  "target_candidate": "TAURUS / ORAN (030°-060°)"},
    {"folio": "f72r1", "spoke_label": "otcheor", "core_stem": "cheor", "voynich_cv": "CVCVC", "target_candidate": "CANCER / PASOR (090°-120°)"},
    {"folio": "f72r1", "spoke_label": "dal",     "core_stem": "l",     "voynich_cv": "C",     "target_candidate": "LEO / L (120°-150°)"},
    {"folio": "f72v1", "spoke_label": "otol",    "core_stem": "ol",    "voynich_cv": "VC",    "target_candidate": "SCORPIO / OR (210°-240°)"},
    {"folio": "f72v2", "spoke_label": "otedy",   "core_stem": "edy",   "voynich_cv": "CCV",   "target_candidate": "SAGITTARIUS / RAM (240°-270°)"},
]

# Codicological Signatures & Author Loci
CODICOLOGICAL_SIGNATURES = [
    {
        "folio": "Folio f1r.6",
        "slot": "=Pt",
        "token": "ydaraishy",
        "description": "Isolated terminal incipit slot formatted like an author attribution in quotations.",
    },
    {
        "folio": "Folio f9r.10",
        "slot": "+Pc",
        "token": "ytchas.oraiin.chkor",
        "description": "Indented quire closure formula (scriptor / blessing / finitus).",
    },
    {
        "folio": "Folio f116v.1",
        "slot": "@Lx",
        "token": "oror sheey",
        "description": "Final codex terminal seal.",
    },
]

# -----------------------------------------------------------------------------
# WORKBENCH NAVIGATION TABS
# -----------------------------------------------------------------------------
tab_matrix, tab_roles, tab_hoax, tab_spokes, tab_colophons, tab_engine, tab_master = st.tabs([
    "Phonetic Matrix",
    "Roles & Macrostates",
    "6. 🏛️ Hoax Falsification & Proofs",
    "Astrological Spokes",
    "7. 🤝 Colophons & Signatures",
    "Translation Engine",
    "8. 💾 Master Dataset",
])

# -----------------------------------------------------------------------------
# Tab 1: 16-Glyph Phonetic Matrix
# -----------------------------------------------------------------------------
with tab_matrix:
    st.subheader("16-Glyph Phonetic & Grammatical Matrix")
    st.markdown("""
| Glyph | Sound | Class | Affix Role |
| :---: | :---: | :---: | :--- |
| **o** | O | Vowel | Prefix operational |
| **t** | T | Vowel | Connective |
| **c** | S | Consonant | Stem core |
| **h** | A | Vowel | Stem nucleus |
| **e** | R | Consonant | Stem core |
| **d** | N | Consonant | Terminal marker |
| **a** | U | Vowel | Stem nucleus |
| **i** | I | Vowel | Iterative inflection |
| **q** | C | Consonant | Prefix procedural |
| **k** | O | Consonant | Thermal marker |
| **p** | M | Consonant | Stem core |
| **m** | S | Consonant | Terminal buffer flush |
| **y** | M | Vowel | Terminal affix |
| **s** | P | Consonant | Stem core |
| **l** | L | Consonant | Liquid coda |
| **r** | R | Consonant | Liquid coda |
""")
    st.markdown("""
    * **Dual-Sound Identifications:**
      * `S` sound: `c` (root consonant) and `m` (terminal buffer flush)
      * `M` sound: `p` (root consonant) and `y` (vocalic/inflection affix)
      * `R` sound: `e` (internal consonant) and `r` (terminal liquid coda)
      * `O` sound: `o` (operational vowel) and `k` (thermal modifier consonant)
    """)

# -----------------------------------------------------------------------------
# Tab 2: Roles & Macrostates
# -----------------------------------------------------------------------------
with tab_roles:
    st.subheader("Distribution")
    st.markdown("""
| Role | Count | Percentage |
| :--- | :---: | :---: |
| **unmapped** | 16,433 | 42.99% |
| **heat** | 7,594 | 19.87% |
| **outlet** | 4,350 | 11.38% |
| **medium** | 4,190 | 10.96% |
| **reflux** | 4,123 | 10.79% |
| **drain** | 1,021 | 2.67% |
| **retain** | 512 | 1.34% |
""")
    st.markdown("---")
    st.markdown("### Sukhotin Vowel Induction")
    st.markdown(r"""
    * **Vocalic Nuclei:** $\{a, o, h, t, i, y\}$
    * **Consonantal Frame:** $\{c, d, e, f, k, l, m, n, p, s, r\}$
    * **Vocalic Ratio:** Evaluates consistently to **33.3%**, conforming strictly to natural Romance/Latin phonotactic balance rather than random numbers or cipher stuffing.
    """)

# -----------------------------------------------------------------------------
# Tab 3: Hoax Falsification & Proofs
# -----------------------------------------------------------------------------
with tab_hoax:
    st.subheader("Model Falsification & Proofs")
    st.markdown(r"""
    * **Line-Preserving `-m` / `-am` Buffer Flush:** Real-world line boundaries force terminal flushes at a rate of 13.3% to 70.0% ($p < 0.001$), decisively falsifying unconstrained prose and proving physical line-register limits.
    * **Rejection of the Timm & Schinner Hoax Generator:** Successor routing asymmetry evaluates to $A_4 = -1.018$ log-odds ($p < 0.00001$), formally ruling out self-citation and mechanical Cardan-grille hoax mechanisms.
    * **Procrustes Manifold Congruence:** The carrier co-occurrence network achieves a **99.79% match** ($d^2 = 0.0021$) against 15th-century Latin pharmaceutical compounding (*Macer Floridus*), while diverging from random controls ($d^2 = 1.489$).
    """)

    st.markdown("---")
    st.markdown("### Procedural Execution Frame: `Q-ACTIVE → [X-aiin] → Q-ACTIVE`")
    st.markdown("""
| Role | Folio | Token |
| :--- | :---: | :--- |
| **medium** | f1r | `ataiin` |
| **medium** | f1r | `chtaiin` |
| **medium** | f1r | `ykaiin` |
| **medium** | f1r | `daraiin` |
| **medium** | f1r | `daiin` |
| **heat** | f1r | `okaiin` |
| **medium** | f1r | `cthaiin` |
| **medium** | f1r | `cfhaiin` |
| **medium** | f1r | `cfhoaiin` |
| **medium** | f1r | `daiin` |
""")

    st.markdown("### Verified Execution Sandwiches:")
    st.markdown("""
    * **Botanical Substrate:** `qokedy` $\\rightarrow$ `chedaiin` $\\rightarrow$ `qokchdy` *(Folio f103r.12)*
    * **Celestial Coordinate:** `qokedy` $\\rightarrow$ `otcheodaiin` $\\rightarrow$ `qokchdy` *(Folio f114v.21)*
    * **Balneological Base:** `qokedy` $\\rightarrow$ `shedaiin` $\\rightarrow$ `qokchdy` *(Folio f76r.05)*
    """)

# -----------------------------------------------------------------------------
# Tab 4: Astrological Spokes
# -----------------------------------------------------------------------------
with tab_spokes:
    st.subheader("Zodiac Spoke Stems & Radial Alignment")
    st.markdown("""
| Folio | Spoke Label | Core Stem | Voynich CV | Target Candidate |
| :---: | :---: | :---: | :---: | :--- |
| **f70v2** | `otcheod` | `cheod` | CVCVC | **PASIS** (Pisces 330°-360°) |
| **f70v2** | `oteodal` | `eodal` | CVCVC | **RADIS** (Pisces Decan 2) |
| **f71r** | `opairam` | `pair` | CVVC | **ARIES / MAUR** (000°-030°) |
| **f71r** | `okeal` | `keal` | CCVC | **TAURUS / ORAN** (030°-060°) |
| **f72r1** | `otcheor` | `cheor` | CVCVC | **CANCER / PASOR** (090°-120°) |
| **f72r1** | `dal` | `l` | C | **LEO / L** (120°-150°) |
| **f72v1** | `otol` | `ol` | VC | **SCORPIO / OR** (210°-240°) |
| **f72v2** | `otedy` | `edy` | CCV | **SAGITTARIUS / RAM** (240°-270°) |
""")

    st.info(
        "**Primary Anchor:** `otcheod` on Pisces (*f70v2*) achieves a 100% consonant-vowel "
        "skeletal lock with **PASIS** (`cvcvc`), anchoring candidate sound values for "
        "`{c, h, e, o, d}`."
    )

# -----------------------------------------------------------------------------
# Tab 5: Colophons & Signatures
# -----------------------------------------------------------------------------
with tab_colophons:
    st.subheader("Codicological Signatures & Author Loci Audit")
    st.markdown("Three structural colophon positions sitting in isolated, right-flushed line ends:")
    st.markdown("""
    * **Folio f1r.6 (=Pt):** `ydaraishy` — Isolated terminal incipit slot formatted like an author attribution in quotations.
    * **Folio f9r.10 (+Pc):** `ytchas.oraiin.chkor` — Indented quire closure formula *(scriptor / blessing / finitus)*.
    * **Folio f116v.1 (@Lx):** `oror sheey` — Final codex terminal seal.
    """)

# -----------------------------------------------------------------------------
# Tab 6: Interactive Translation Engine
# -----------------------------------------------------------------------------
with tab_engine:
    st.subheader("Interactive Folio Reader & Dual-Dialect Translation Engine")

    with st.expander("Folio f114v Line 4 — Distillation Procedure", expanded=True):
        st.markdown("**Raw IVTFF:** `qokedy cheocthedy qoted chedar okeedy daiin chedaiin oky chdam`")
        st.markdown("**Venetian Pharmacy:** `coci fraturo de erba scalda fiori d'erba incorpora agva decocto d'erba saldo`")
        st.markdown("**Early German Pharmacy:** `sied kruttheil waerme bluemen menge wazzer krutwazzer beschliess`")
        st.info("**Synthesized Reading:** Boil the plant fraction, warm the blossoms, compound with water menstruum and herb decoction, and seal the vessel.")

    with st.expander("Folio f114v Line 21 — Cross-Modal Celestial Handoff", expanded=True):
        st.markdown("**Raw IVTFF:** `qokedy otcheodaiin qokchdy`")
        st.markdown("**Venetian Pharmacy:** `coci licore de stella coci_qokchdy`")
        st.markdown("**Early German Pharmacy:** `sied sternauszug sied_qokchdy`")
        st.info("**Synthesized Reading:** Heat the astronomical sector component; proceed immediately into active secondary boiling cycle.")

    with st.expander("Folio f103r Line 12 — Botanical Substrate Compounding", expanded=False):
        st.markdown("**Raw IVTFF:** `qokedy chedaiin qokchdy`")
        st.markdown("**Venetian Pharmacy:** `coci decocto coci_qokchdy`")
        st.markdown("**Early German Pharmacy:** `sied krutwazzer sied_qokchdy`")
        st.info("**Synthesized Reading:** Boil the herbal decoction substrate and proceed immediately to secondary heat.")

    with st.expander("Folio f76r Line 05 — Balneological Menstruum Preparation", expanded=False):
        st.markdown("**Raw IVTFF:** `qokedy shedaiin qokchdy`")
        st.markdown("**Venetian Pharmacy:** `coci bagno_minerale coci_qokchdy`")
        st.markdown("**Early German Pharmacy:** `sied mineralbad sied_qokchdy`")
        st.info("**Synthesized Reading:** Heat the mineral bath base and proceed to the secondary boiling cycle.")

# -----------------------------------------------------------------------------
# Tab 7: Master Dataset & Codicological Index
# -----------------------------------------------------------------------------
with tab_master:
    st.subheader("Master Decipherment Dataset & Audit Summary")
    st.markdown("""
    This master workbench integrates:
    1. **Empirical Hardware Proofs:** Rejection of mechanical grille generators ($A_4 = -1.018$) and 99.79% match to *Macer Floridus*.
    2. **Sukhotin Vowel Induction:** 33.3% Romance/Latin natural vowel balance across the corpus.
    3. **The 30-Degree Radial Wheel:** Primary anchor `otcheod` $\\rightarrow$ `PASIS` on Pisces ($f70v2$).
    4. **Procedural Execution Sandwiches:** Systematic `Q-ACTIVE → [X-aiin] → Q-ACTIVE` operational grammar.
    5. **Codicological Loci:** Verified incipit ($f1r.6$), quire closure ($f9r.10$), and terminal seal ($f116v.1$).
    """)
    st.dataframe(pd.DataFrame(PHONETIC_MATRIX_DATA), use_container_width=True, hide_index=True)
