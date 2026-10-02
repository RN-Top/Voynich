# Pre-registration: are the pharmacy plant-part labels plant names?

Committed 2026-10-02, **before** the test below is run. Amend only below the line at the end.

## Idea

Decoding needs anchors, words whose meaning can be pinned down. The pharmacy pages (f88–f102) label
individual plant parts (ZL3b locus code Lf), and many of those plants also appear as full drawings in the herbal
section. If a label is the **name** of the plant, the same word should turn up in the herbal text, and it
should be **concentrated on the page of that plant** (its own entry), unlike ordinary words, which spread
across many pages.

## Data

- Label words: every word in the Lf labels, cleaned with the canonical cleaner, at least 4 letters long.
- Herbal text: paragraph text (locus P) on Herbal-section pages, Currier A and B together.

## A1. Are label words concentrated like names?

For each distinct label word w seen at least twice in herbal text (n = its herbal count),
concentration(w) = (count on its most frequent herbal page) / n.

Statistic: mean concentration over these label words.

Null: for each label word, draw a herbal word that is **not** a label word, with the same herbal count n (or the
nearest count available), and take its concentration. The mean over all label words is one null draw. There are
10,000 draws, seed 20261002. Pass: p < 0.01. If fewer than 10 label words qualify, the result is "too few to
test".

## A2. Candidate anchors (descriptive, not a test)

Candidate list: label words found in herbal text (any count), with concentration ≥ 0.5, ranked by
concentration and then count. For the top candidates, the pharmacy page with the label and the herbal page
where the word concentrates are shown side by side from the Yale PDF, so the drawings can be compared. That
comparison is an impression, not a test. A candidate becomes an anchor only if a later, separately
pre-registered test confirms it.

---
Amendments (dated, below this line only):
