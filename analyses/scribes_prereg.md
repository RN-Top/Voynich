# Pre-registration: scribe vs topic, and whether the rules hold for every scribe

Committed 2026-10-03, **before** the test below is run. Amend only below the line at the end.

## Why

ZL3b tags each page with one of five scribes (`$H=1…5`, after L. Fagin Davis 2020). Scribe and section overlap
almost completely: scribe 1 wrote most herbal pages (Currier A) and pharmacy pages; scribe 2 bath, cosmological and
some herbal pages; scribe 3 the recipe pages plus some herbal and pharmacy pages; scribe 4 the astronomical pages;
scribe 5 seven herbal pages. So "topic" differences found earlier could be "writer" differences. Two contrasts
separate them: herbal pages written by different scribes (topic fixed, writer varies), and single scribes writing
different sections (writer fixed, topic varies).

## Data

Paragraph text (locus P), with roots from `analyses/root_dictionary_test.py`. Roots with fewer than 5 tokens in the
subset analysed are pooled as "rare".

## Tests (2,000 page shuffles each, seed 20261003)

- **S1, writer effect with topic fixed.** Herbal pages only: MI between root and scribe. Null: scribe labels
  shuffled among herbal pages. Pass: p < 0.01.
- **S2, topic effect with writer fixed.** For each scribe who wrote at least two sections with at least 500 words
  each (scribe 1: herbal/pharmacy; scribe 2: bath/cosmological/herbal; scribe 3: recipes/herbal/pharmacy): MI
  between root and section, with sections shuffled among that scribe's pages. Each scribe tested at p < 0.01/3.
  The topic effect is **confirmed** if at least one scribe passes.
- **S3, do the rules hold for every scribe?** For each scribe with at least 1,500 interior word pairs: word order
  carries information (interior-pair MI against within-line shuffles, 1,000 shuffles, p < 0.01), and the strongest
  grammar link is ending → next beginning (as in `analyses/phrases_test.py`, 500 shuffles). The rules are
  **universal** if every qualifying scribe shows both.

## Descriptive

A profile of each scribe: words, common beginnings and endings, mean word length, and rare symbols per 1,000
words.

---
Amendments (dated, below this line only):

**2026-10-03, results.** S1 PASS (p = 0.0005). S2: scribes 1 and 2 PASS, scribe 3 FAIL (p = 0.014); topic effect
confirmed. S3: rules universal across scribes 1–3 (4 and 5 have too little text). Write-up: `output/scribes_report.md`.
