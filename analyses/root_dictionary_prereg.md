# Pre-registration: a root dictionary (which word cores belong to which section?)

Committed 2026-10-02, **before** the test below is run. Amend only below the line at the end.

## Background

Word beginnings track a page's section (`output/writing_types_report.md`), and plant-page openings share roots with
star labels (`output/plant_star_report.md`). This builds a list of word **roots** and asks which belong to particular
sections. Those are candidate dictionary entries.

## Root rule (fixed in advance)

From the canonical clean word: remove a leading "q", then a leading "o", then a leading "y", each at most once and
in that order. Then remove the longest matching ending from the parser's ending list
(`structural_validation.ENDINGS`: am, m, eedy, edy, eey, ey, dy, aiiin, aiin, ain, or, ar, ol, al, y). What remains is
the root; if nothing remains, the root is "∅".

Examples: qokedy → k; okoaly → koal; chedy → ch; daiin → d.

## Data

Paragraph text (locus P), sections from the parser.

## Tests

- **T1 (do roots follow the topic?).** Mutual information between root and section. Roots with fewer than 5 tokens
  are pooled as "rare". Null: section labels shuffled between pages within each Currier language (2,000 shuffles,
  seed 20261002). Pass: p < 0.01.
- **T2 (dictionary entries).** For each root with at least 10 tokens: the share of its tokens in its most frequent
  section, compared with the same page shuffles, giving one p per root. Roots passing a Benjamini–Hochberg false
  discovery rate of 5% are listed as **section roots**, with their section, their count and example words.

## Descriptive

Roots that occur both in herbal-page opening words and in star labels.

---
Amendments (dated, below this line only):

**2026-10-02, results.** T1 PASS (0.214 vs 0.103 bits, p = 0.0005). T2: 23 of 256 roots pass FDR 5%, all in
Stars/Recipes or Biological. The report's baseline column is over the whole book; the correct within-Currier-B
shares (46%, 29%) are added in the reading. Write-up: `output/root_dictionary_report.md`.
