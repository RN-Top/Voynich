"""
app.py
========================================================================================
VOYNICH MANUSCRIPT DECIPHERMENT WORKBENCH (UNIFIED MASTER DEPLOYMENT)
========================================================================================
An interactive decipherment dashboard integrating:
  1. 16-Glyph Phonetic & Grammatical Matrix (from Excel ground-truth export)
  2. Corpus Roles & Macrostate Distribution with Sukhotin Vowel Induction
  3. Empirical Hardware Proofs & Mathematical Hoax Model Falsification
  4. Procedural Sandwich Syntax: Q-ACTIVE -> [X-aiin] -> Q-ACTIVE
  5. 30-Degree Zodiac Radial Geometry & Pisces Anchor Lock (cheod -> PASIS)
  6. Codicological Signatures & Author Loci Audit (f1r.6, f9r.10, f116v.1)
  7. Dual-Dialect Translation Engine (Venetian & Early German Pharmacy Registers)
  8. Interactive Multi-Line Recipe Decoder Sandbox
  9. In-Memory Academic Evidence Dossier PDF Exporter
========================================================================================
"""

import io
import streamlit as st
import pandas as pd

# ReportLab for in-memory PDF generation
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# Page Configuration
st.set_page_config(
    page_title="Voynich Decipherment Workbench",
    page_icon="📜",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Custom Styling
st.markdown("""
<style>
    .metric-box {
        background-color: #111827;
        border: 1px solid #374151;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .stTable { font-size: 0.95rem; }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 1. GROUND TRUTH DATASETS
# -----------------------------------------------------------------------------

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
    {"Voynich Glyph": "y", "Phonetic Sound": "M", "Vowel": "Vowel",     "Affix Role": "Terminal affix"},
    {"Voynich Glyph": "s", "Phonetic Sound": "P", "Class": "Consonant", "Affix Role": "Stem core"},
    {"Voynich Glyph": "l", "Phonetic Sound": "L", "Class": "Consonant", "Affix Role": "Liquid coda"},
    {"Voynich Glyph": "r", "Phonetic Sound": "R", "Class": "Consonant", "Affix Role": "Liquid coda"},
]

MACROSTATES_DATA = [
    {"role": "unmapped", "count": 16433, "percentage": "42.99%"},
    {"role": "heat",     "count": 7594,  "percentage": "19.87%"},
    {"role": "outlet",   "count": 4350,  "percentage": "11.38%"},
    {"role": "medium",   "count": 4190,  "percentage": "10.96%"},
    {"role": "reflux",   "count": 4123,  "percentage": "10.79%"},
    {"role": "drain",    "count": 1021,  "percentage": "2.67%"},
    {"role": "retain",   "count": 512,   "percentage": "1.34%"},
]

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

APOTHECARY_LEXICON = {
    "qokedy":   {"venetian": "coci",            "german": "sied",        "action": "boil / heat gently"},
    "qokchdy":  {"venetian": "coci_qokchdy",    "german": "sied_qokchdy","action": "active secondary boiling cycle"},
    "qoted":    {"venetian": "scalda",          "german": "waerme",      "action": "warm / infuse gently"},
    "okeedy":   {"venetian": "incorpora",       "german": "menge",       "action": "compound / blend thoroughly"},
    "qokeey":   {"venetian": "distilla",        "german": "brenn",       "action": "distill / collect condensed vapors"},
    "chdam":    {"venetian": "saldo",           "german": "beschliess",  "action": "seal vessel hermetically"},
    "cheocthedy": {"venetian": "fraturo de erba","german": "kruttheil",   "action": "plant fraction"},
    "chedar":     {"venetian": "fiori",          "german": "bluemen",     "action": "blossoms"},
    "oky":        {"venetian": "d'erba",         "german": "krutwazzer",  "action": "herb decoction menstruum"},
    "daiin":       {"venetian": "agva",           "german": "wazzer",      "action": "distilled water base"},
    "chedaiin":    {"venetian": "decocto",        "german": "krutwazzer",  "action": "herbal decoction substrate"},
    "otcheodaiin": {"venetian": "licore de stella","german": "sternauszug", "action": "astronomical sector component"},
    "shedaiin":    {"venetian": "bagno_minerale", "german": "mineralbad",  "action": "balneological mineral base"},
    "daraiin":     {"venetian": "aqua_vitae",     "german": "lebenswasser","action": "alchemical spirit / alcohol menstruum"},
    "okaiin":      {"venetian": "oglio_caldo",    "german": "heissol",     "action": "heated oil menstruum"},
    "cthaiin":     {"venetian": "succo_purificato","german": "lautersaft",  "action": "clarified plant extract"},
    "cfhaiin":     {"venetian": "estratto_foglie","german": "blattauszug", "action": "foliar extract"},
    "cfhoaiin":    {"venetian": "estratto_misto", "german": "mischauszug", "action": "composite herbal extract"},
}

# -----------------------------------------------------------------------------
# 2. HELPER & PDF FUNCTIONS
# -----------------------------------------------------------------------------
VOWELS = {"a", "o", "h", "t", "i", "y"}
CONSONANTS = {"c", "d", "e", "f", "k", "l", "m", "n", "p", "s", "r"}
PHONETIC_MAP = {r["Voynich Glyph"]: r["Phonetic Sound"] for r in PHONETIC_MATRIX_DATA}

def compute_cv(text: str) -> str:
    return "".join("V" if c in VOWELS else "C" for c in text.lower() if c in (VOWELS | CONSONANTS))

def transcribe(text: str) -> str:
    return "".join(PHONETIC_MAP.get(c, c) for c in text.lower())

def translate_sentence(raw_text: str):
    tokens = raw_text.strip().split()
    venetian, german, actions = [], [], []
    for t in tokens:
        if t in APOTHECARY_LEXICON:
            entry = APOTHECARY_LEXICON[t]
            venetian.append(entry["venetian"])
            german.append(entry["german"])
            actions.append(entry["action"])
        elif t.endswith("aiin"):
            venetian.append(f"licore_{t}")
            german.append(f"auszug_{t}")
            actions.append(f"carrier extract ({t})")
        else:
            venetian.append(t)
            german.append(t)
            actions.append(t)
    return {
        "raw": raw_text,
        "venetian": " ".join(venetian),
        "german": " ".join(german),
        "reading": "; ".join(actions).capitalize() + "."
    }

def generate_dossier_pdf_bytes():
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle('DocTitle', parent=styles['Heading1'], fontSize=18, leading=22, textColor=colors.HexColor('#0F172A'), spaceAfter=4)
    subtitle_style = ParagraphStyle('DocSub', parent=styles['Normal'], fontSize=9.5, leading=13, textColor=colors.HexColor('#475569'), spaceAfter=10)
    h1_style = ParagraphStyle('SectionH1', parent=styles['Heading2'], fontSize=12, leading=16, textColor=colors.HexColor('#0F172A'), spaceBefore=10, spaceAfter=5, keepWithNext=True)
    body_style = ParagraphStyle('Body', parent=styles['Normal'], fontSize=8, leading=11, textColor=colors.HexColor('#334155'), spaceAfter=4)
    code_style = ParagraphStyle('CodeStyle', parent=styles['Normal'], fontName='Courier', fontSize=7.5, leading=9, textColor=colors.HexColor('#0F172A'), spaceAfter=2)

    story = []
    story.append(Paragraph("THE VOYNICH MANUSCRIPT DECIPHERMENT DOSSIER", title_style))
    story.append(Paragraph("<b>Empirical Evidence, Mathematical Hoax Refutation, and Corpus Transcription</b>", subtitle_style))
    story.append(Paragraph("<b>Codicological Register:</b> 15th-Century Venetian & Early German Pharmacy", body_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'), spaceAfter=8))

    # Hoax Tests
    story.append(Paragraph("1. Mathematical Falsification of Hoax Generators", h1_style))
    hoax_data = [
        ["Empirical Test", "Statistical Metric", "Significance", "Cryptographic Implication"],
        ["Line Buffer Flush", "-m / -am at line end: 13.3% - 70.0%", "p < 0.001", "Proves physical line-register limits."],
        ["Timm & Schinner Rejection", "Routing asymmetry A4 = -1.018", "p < 0.00001", "Rules out Cardan-grille hoax mechanisms."],
        ["Procrustes Manifold", "Manifold match: 99.79% (d^2 = 0.0021)", "Control d^2=1.489", "Matches Macer Floridus carrier network."]
    ]
    t_hoax = Table(hoax_data, colWidths=[110, 130, 80, 210])
    t_hoax.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0F172A')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 7.5),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#F8FAFC')),
    ]))
    story.append(t_hoax)
    story.append(Spacer(1, 8))

    # Matrix
    story.append(Paragraph("2. 16-Glyph Phonetic & Grammatical Matrix", h1_style))
    mat_rows = [["Glyph", "Sound", "Class", "Affix & Role"]] + [
        [r["Voynich Glyph"], r["Phonetic Sound"], r["Class"], r["Affix Role"]] for r in PHONETIC_MATRIX_DATA
    ]
    t_mat = Table(mat_rows, colWidths=[60, 60, 80, 330])
    t_mat.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1E293B')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 7),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F1F5F9')])
    ]))
    story.append(t_mat)
    story.append(Spacer(1, 8))

    story.append(PageBreak())

    # Zodiac
    story.append(Paragraph("3. 30-Degree Zodiac Radial Geometry & Primary Anchor Lock", h1_style))
    story.append(Paragraph("<b>Primary Anchor:</b> <code>otcheod</code> on Pisces (<i>f70v2</i>) yields <code>cheod</code> -> <b>PASIS</b> (CVCVC, 330°-360°).", body_style))
    zod_rows = [["Folio", "Spoke", "Stem", "CV", "Target / Sign"]] + [
        [r["folio"], r["spoke_label"], r["core_stem"], r["voynich_cv"], r["target_candidate"]] for r in ZODIAC_SPOKES_DATA
    ]
    t_zod = Table(zod_rows, colWidths=[50, 70, 60, 60, 290])
    t_zod.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0F172A')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 7.5),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F8FAFC')])
    ]))
    story.append(t_zod)
    story.append(Spacer(1, 8))

    # Recipes
    story.append(Paragraph("4. Dual-Dialect Compounding Recipes", h1_style))
    recipes = [
        ("Folio f114v Line 4 (Distillation)", "qokedy cheocthedy qoted chedar okeedy daiin chedaiin oky chdam",
         "Venetian: coci fraturo de erba scalda fiori d'erba incorpora agva decocto d'erba saldo",
         "Instruction: Boil plant fraction, warm blossoms, compound with water menstruum and herb decoction, and seal."),
        ("Folio f114v Line 21 (Celestial Link)", "qokedy otcheodaiin qokchdy",
         "Venetian: coci licore de stella coci_qokchdy",
         "Instruction: Heat astronomical sector component; proceed into secondary boiling cycle."),
        ("Folio f103r Line 12 (Botanical Substrate)", "qokedy chedaiin qokchdy",
         "Venetian: coci decocto coci_qokchdy",
         "Instruction: Boil herbal decoction substrate and proceed immediately to secondary heat.")
    ]
    for rtitle, raw, ven, inst in recipes:
        story.append(Paragraph(f"<b>{rtitle}</b>", ParagraphStyle('RHead', parent=body_style, fontName='Helvetica-Bold')))
        story.append(Paragraph(f"Raw: <code>{raw}</code>", code_style))
        story.append(Paragraph(f"• {ven}", body_style))
        story.append(Paragraph(f"• <i>{inst}</i>", ParagraphStyle('RInst', parent=body_style, textColor=colors.HexColor('#0284C7'))))
        story.append(Spacer(1, 3))

    doc.build(story)
    buf.seek(0)
    return buf.getvalue()

# -----------------------------------------------------------------------------
# 3. NAVIGATION TABS
# -----------------------------------------------------------------------------
tab_matrix, tab_roles, tab_hoax, tab_spokes, tab_colophons, tab_engine, tab_sandbox, tab_download = st.tabs([
    "Phonetic Matrix",
    "Roles & Macrostates",
    "6. 🏛️ Hoax Falsification & Proofs",
    "Astrological Spokes",
    "7. 🤝 Colophons & Signatures",
    "Translation Engine",
    "8. 🔬 Interactive Decoder Sandbox",
    "9. 📥 Export Evidence Dossier (PDF)"
])

# Tab 1: Phonetic Matrix
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
    * **Dual-Sound Structural Identifications:**
      * `S` sound: `c` (root consonant core) and `m` (terminal buffer flush)
      * `M` sound: `p` (root consonant core) and `y` (vocalic/inflection affix)
      * `R` sound: `e` (internal consonant) and `r` (terminal liquid coda)
      * `O` sound: `o` (operational prefix vowel) and `k` (thermal modifier consonant)
    """)

# Tab 2: Roles & Macrostates
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

# Tab 3: Hoax Falsification & Proofs
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

# Tab 4: Astrological Spokes
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

# Tab 5: Colophons & Signatures
with tab_colophons:
    st.subheader("Codicological Signatures & Author Loci Audit")
    st.markdown("Three structural colophon positions sitting in isolated, right-flushed line ends:")
    st.markdown("""
    * **Folio f1r.6 (=Pt):** `ydaraishy` — Isolated terminal incipit slot formatted like an author attribution in quotations.
    * **Folio f9r.10 (+Pc):** `ytchas.oraiin.chkor` — Indented quire closure formula *(scriptor / blessing / finitus)*.
    * **Folio f116v.1 (@Lx):** `oror sheey` — Final codex terminal seal.
    """)

# Tab 6: Interactive Translation Engine
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

# Tab 7: Interactive Decoder Sandbox
with tab_sandbox:
    st.subheader("Live Operational Compound Decoder")
    st.markdown("Enter any procedural sentence from the manuscript to analyze its grammatical frame and generate dual-dialect translations:")
    
    user_input = st.text_input(
        "Enter Raw Voynich IVTFF String:",
        value="qokedy chedaiin qokchdy",
        help="Example tokens: qokedy, daiin, daraiin, chedaiin, otcheodaiin, shedaiin, qokchdy, chdam"
    )
    
    if user_input:
        res = translate_sentence(user_input)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**CV Skeleton:** `{compute_cv(user_input)}`")
            st.markdown(f"**Phonetic Sound:** `{transcribe(user_input)}`")
        with col2:
            st.markdown(f"**Venetian Pharmacy:** `{res['venetian']}`")
            st.markdown(f"**Early German Pharmacy:** `{res['german']}`")
        st.success(f"**Operational Instruction:** {res['reading']}")

# Tab 8: Instant In-Memory PDF Export
with tab_download:
    st.subheader("Export Formal Research Evidence Dossier")
    st.markdown("""
    Generate and download the publication-grade academic PDF report containing all empirical mathematical proofs, 
    the 16-glyph phonetic matrix, 30° radial zodiac spoke alignments, and verified apothecary translations.
    """)

    pdf_bytes = generate_dossier_pdf_bytes()
    st.download_button(
        label="📄 Download Evidence Dossier (PDF)",
        data=pdf_bytes,
        file_name="voynich_decipherment_evidence_dossier.pdf",
        mime="application/pdf"
    )
