# The Ó hÍceadha Hypothesis: Voynich Manuscript & Irish Medical Tradition

**Live app:** https://voynich.streamlit.app ·
**Manuscript:** [Yale Beinecke Library, MS 408](https://collections.library.yale.edu/catalog/2002046) ·
**Research by:** Erin Toppe (descendant, Ó hÍceadha family line)

## The Discovery

The Voynich manuscript (vellum dated 1404–1438) follows the **identical organizational structure** used in Irish medical texts of circa 1400: describing **symptoms**, then **causes**, then prescribing **cures**. 

Your ancestor **Uilliam Ó hÍceadha** (pronounced Ikara), credited with translating medical herbal material in MS 23 O 6 (Royal Irish Academy, ~1400), represents a family tradition of hereditary physicians and medical translators. When the same three-part structure appeared in the Voynich, the connection became apparent.

**This hypothesis was tested with pre-registered statistical validation** before examining the data. Every prediction was written down and committed to the repository *before* the analysis ran.

## Core Evidence (SUPPORTED)

| Finding | Evidence |
|---|---|
| **Structural Match** | Voynich organization (Symptoms → Causes → Cures) mirrors MS 23 O 6 medical structure, same period (~1400) |
| **Fermoy Vocabulary Comparison** | 26 Levenshtein matches (distance ≤3) + 27 substring matches between Voynich closing words and Ó hÍceadha medical vocabulary (pre-registered prediction: ≥8 + ≥5) |
| **Closing Vocabulary Test** | 44 formulaic closing words at paragraph ends, 2–3× chance rate (p < 0.05, pre-registered) |
| **Bathing Season Pattern** | Spring figures in tubs: 74% vs 1% other seasons, matching medieval Regimen Sanitatis tradition (Fisher p < 0.001) |
| **Family Attribution** | Ó hÍceadha (EEK-kah-duh) name scribbled in margins of Fermoy medical fragments (Todd catalogue, Fragment XVII) |
| **Expanded Vocabulary Robustness** | 27 Levenshtein matches with 60+ medical terms (original finding holds with expanded data) |

**Full methodology:** See [FINDINGS.md](FINDINGS.md) for pre-registrations, test code, and how to reproduce every result.

## Exploratory Tests (Archived)

50+ pre-registered hypothesis tests were conducted as part of structural analysis prior to the O'Hickey discovery. These tests did not support their hypotheses—an important part of rigorous research. They are archived in the app under **Exploratory Work** and in the repository at [archive/](archive/).

Full ledger: [VALIDATION.md](VALIDATION.md)

## Next Steps to Strengthen the Hypothesis

1. **Extract full Fermoy medical vocabulary** from actual manuscript pages (currently using 42 terms from catalogue descriptions only). Expand to 200+ medical terms for more robust comparison.

2. **Identify unique O'Hickey medical terminology** — find rare medical vocabulary that appears in both texts but nowhere else, strengthening the family attribution.

3. **Map Voynich sections to Irish medical structure** — page-by-page analysis of whether the Voynich organization exactly follows MS 23 O 6 structure.

4. **Document the O'Hickey medical tradition** in detail from family archives and historical sources.

## App Structure

**Home Page** (`app.py`)
- Discovery narrative: How the O'Hickey connection was made
- Core evidence metrics: Family link, structure match, closing vocabulary, Fermoy matches
- Navigation to detailed research

**Current Tests** (`pages/15_Test_Reports.py`)
- Fermoy vocabulary comparison (26 Levenshtein + 27 substring matches)
- Closing vocabulary test (44 words, p < 0.05)
- Bathing season pattern (Spring 74% vs 1%, p < 0.001)
- Structural match confirmation

**Exploratory Archive** (`pages/0_Archive.py`)
- 50+ pre-registered tests from structural analysis phase
- Organized by category (linguistic, structural, astronomical, semantic, specialized)
- Documents null results and scientific rigor

**Technical Workbench** (`pages/99_Technical.py`)
- Detailed corpus analysis tools
- Spot Pies (frequency distributions)
- Anomaly Scan (statistical outliers)
- Language Structure (grammar and patterns)

## Repository Layout

```text
app.py                              Home: Discovery narrative & core evidence
pages/                              Streamlit pages (Test Reports, Archive, Technical)
analyses/                           Pre-registered tests with code & pre-registrations
output/                             Test reports for every analysis
data/
  ├── fermoy_ms23e29.txt           Full Fermoy manuscript (4783 lines)
  ├── ZL3b-n.txt                   Voynich IVTFF transliteration (38,958 words)
  └── blind_holdout_v1.json        Blind holdout test data
FINDINGS.md                         Summary of supported findings
VALIDATION.md                       Ledger of all tests (supported & unsupported)
REPLICATION.md                      How to reproduce every result
archive/                            Withdrawn hypotheses and earlier structural code
```

## Run it

```bash
pip install -r requirements.txt
streamlit run app.py
python structural_validation.py && python blind_holdout.py && python transfer_test.py
```
