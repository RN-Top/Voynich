# Pre-registration: does the text on a page mention that page's labels? (a "ground" test)

Committed 2026-10-02, **before** the test below is run. Amend only below the line at the end.

## Idea

Labels sit next to specific drawn things (a woman, a pool, a jar, a plant part, a star). If the paragraph text on the
same page talks about what is drawn, the label words should appear in **their own page's** paragraph text more
often than in the paragraph text of other pages of the same section. That would tie the text to the pictures, the
first "ground" connection between the writing and the world.

## Data

- Labels: every ZL3b label locus (code L…) on a page that also has paragraph text (locus P). Each word in a label,
  cleaned, at least 3 letters long. Sections use the parser's section field.
- Paragraph text: locus P on the same pages.

## Statistic

Number of label words that also occur in the paragraph text of their own page (each label word counted once per
label).

## Null

Labels are shuffled between pages **of the same section**, keeping each page's number of labels (10,000 shuffles,
seed 20261002). This keeps section vocabulary and label counts fixed, so only "this page" vs "another page like it"
changes.

## Tests

- **G1, bath pages (Biological section).** The pre-registered primary test, where the repeated formulas are.
- **G2, all sections together** (shuffled within each section).

Pass: p < 0.01 for each.

## Decision

- **Supported (ground found):** G1 or G2 passes. The label words that hit, and their pages, are listed.
- **Not supported:** neither passes.

---
Amendments (dated, below this line only):

**2026-10-02, results.** G1 FAIL (24 vs 23.2, p = 0.45). G2 FAIL (60 vs 58.2, p = 0.38). **Not supported.**
Write-up: `output/ground_report.md`.
