# Replication guide

This guide is for an independent group that wants to reproduce, or try to break, the structural
results in this repository. Everything runs offline on a laptop in under a minute.

## 1. Get the exact inputs

```bash
git clone https://github.com/RN-Top/Voynich.git
cd Voynich
sha256sum data/ZL3b-n.txt data/blind_holdout_v1.json
# 3e617b2dd4c17736…  data/ZL3b-n.txt            (ZL3b transliteration, version of 13/05/2025)
# b3a17a0c4c49f49b…  data/blind_holdout_v1.json (pre-registered holdout, do not edit)
```

The tested setup used Python 3.11, numpy 2.4, pandas 3.0, scipy 1.17 and streamlit 1.64. Other recent
versions should give the same numbers, up to permutation noise in the third decimal of p-values.

```bash
pip install -r requirements.txt
```

## 2. Run the three scripts

```bash
python structural_validation.py   # ~15 s → output/structural_validation_report.md
python blind_holdout.py           # ~2 s  → output/blind_holdout_report.md
python transfer_test.py           # ~20 s → output/transfer_report.md
```

All randomness is seeded. Compare your output with the committed copies in `output/`.

## 3. What you should get

| Result | Expected |
|---|---|
| Paragraph tokens ending -m/-am that are line-final | 605 / 861 (OR ≈ 20.7, within-line shuffle p ≈ 5e-5) |
| C→L→P→R vs Markov-1 / Markov-2 twins | not significant (p ≈ 0.1 / 0.4) |
| Affix-role tournament (published grouping vs shuffled groupings) | p ≈ 0.99 (not selected) |
| Semantic permutation tournament | p ≈ 0.4 (glosses not supported) |
| Blind A: line-final token on 43 unseen folios | AUC 0.671, p ≈ 0.0005 |
| Blind B: label/diagram vs paragraph | AUC 0.635, p ≈ 0.0005 |
| Blind C: section of folio | 65.1%, ties the majority guess (fail) |
| Blind D: stem predicts its ending | 0.775 bits/token, p ≈ 0.001 |

## 4. What is frozen

- **Tokenisation and morphology:** `parser.py`. `parse_zl3b()` with default arguments is the canonical
  representation.
- **State rules:** `parser.VoynichParser.map_macrostate`. `structural_validation.ending_of` reproduces
  them exactly (the affix-role test checks this and reports 0 mismatches).
- **Holdout:** `data/blind_holdout_v1.json`. It was committed in `68952a4`, before the scorer
  (`a266ebc`) existed. Target D was committed in `3b74dd5`, before its first run.

Please do not tune rules against holdout v1. If the rules change, draw a fresh holdout (v2) with a new
seed and commit it before scoring.

## 5. The most useful independent checks

1. **Another transcription.** Download a different IVTFF transliteration, for example Takahashi's
   `IT2a-n.txt` from https://www.voynich.nu/data/, then run
   `python transfer_test.py --corpus IT2a-n.txt`. Or upload the file in the app's sidebar, which
   reruns every tab on it.
2. **Your own parser.** Re-implement tokenisation from the IVTFF specification without using
   `parser.py`, and check the -m/-am and blind A/B results.
3. **Different nulls.** Try nulls we did not use, for example the Timm & Schinner self-citation
   generator, or a word-level Markov model with matched line lengths.

Please send results either way, including failures. A failed replication is as useful as a successful one.
