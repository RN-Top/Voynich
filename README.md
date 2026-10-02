# Voynich Manuscript (Beinecke MS 408): Structural Workbench

**Live app:** https://voynich.streamlit.app ·
**Images:** [Yale Beinecke Library, MS 408](https://collections.library.yale.edu/catalog/2002046) ·
**Text:** ZL3b IVTFF transliteration (`data/ZL3b-n.txt`, 38,958 words via `parser.py`)

This project studies the **structure** of the Voynich text: how its words are built and where they sit on the
page. It does not offer a translation. Every result below was tested against chance and against simpler
explanations. The strongest were tested on 43 pages chosen at random and committed to the repository
*before* any scoring code existed.

## What holds up

| Finding | Evidence |
|---|---|
| **Line-final -m / -am.** Words ending in -m/-am strongly prefer the end of a physical line. | 605 of 861 paragraph-text cases are line-final (odds ratio ≈ 21; within-line shuffle p ≈ 5e-5). |
| **It behaves like a scribal line-end habit**, not an end-of-section marker. | Half as common at paragraph ends (8.5% vs 16.1%, p ≈ 1e-4; pre-registered test). |
| **Endings predict position on unseen pages.** | Blind holdout: line-final AUC 0.67, label vs paragraph AUC 0.64 (both p ≈ 5e-4). |
| **Stems predict their endings on unseen pages.** | 0.78 bits per word (p ≈ 0.001, blind holdout). |
| **Each folded sheet was written as a unit.** | Sheet halves share more vocabulary than other page pairs, also within the same scribe and dialect (pre-registered, p ≈ 1e-4). |
| **The results don't depend on transcription choices.** | All verdicts unchanged on a second representation of the text. |
| **Not plain Latin, nor a simple letter cipher of Latin.** | Character predictability and word length differ (exploratory comparison). |

## Tested and not supported

These ideas were tested and did not hold up. Their code is kept in [`archive/`](archive/), and the full results
are in [VALIDATION.md](VALIDATION.md).

- Venetian / German procedural translations (the semantic permutation test fails, p ≈ 0.4)
- The C → L → P → R four-state cycle (no better than simpler Markov patterns)
- The front/back/center fold as a key (fold overlays match no better than ordinary pages)
- Zodiac figure labels as day names (p ≈ 0.76)
- The earlier 90.2% "blind" score, the 99.79% Macer Floridus match, and Δ = −1.018 (withdrawn; see VALIDATION.md)

## Open leads

- **Key-like pages:** f57v and f49v (also found independently by the anomaly scan), and the Roman-letter
  column in the f1r margin.
- **f67r2:** stroke marks around the rim that the transcription does not record ([IMAGE_NOTES.md](IMAGE_NOTES.md)).
- **Next steps:** an independent transcription (Takahashi), medieval Italian or German comparison texts,
  and outside replication ([REPLICATION.md](REPLICATION.md)).

## Repository layout

```text
app.py                      Streamlit workbench: Findings, Blind Holdout, Token Breakdown,
                            Verification Suite, Slot Ω Miner, Folio Reader, Export
pages/                      Spot Pies, Anomaly Scan
parser.py                   Canonical IVTFF parser used everywhere
structural_validation.py    Meaning-free validation ladder
blind_holdout.py            Pre-registered blind holdout (data/blind_holdout_v1.json)
transfer_test.py            Same tests on another representation / transcription
analyses/                   Pre-registered and exploratory studies (with their pre-registrations)
output/                     Reports for every test
VALIDATION.md               What passed, what failed, and why
REPLICATION.md              How to reproduce every number
IMAGE_NOTES.md              Observations from the manuscript photos
archive/                    Withdrawn hypotheses and earlier code, kept for the record
```

## Run it

```bash
pip install -r requirements.txt
streamlit run app.py
python structural_validation.py && python blind_holdout.py && python transfer_test.py
```
