# Pre-registration: do the bath-page roots appear in the bath-picture labels?

Committed 2026-10-02, **before** the test below is run. Amend only below the line at the end.

## Background

`output/root_dictionary_report.md` found four roots concentrated in Biological (bath-page) paragraph text:
**rsh, sheckh, lsh, lch**. If these roots are about what the bath pages show (water, pools, bathing, the women), they
should appear in the **labels on the bath pictures** more than in labels elsewhere.

## Data

Every word of every label locus (ZL3b, codes L…), canonical clean. Roots are taken with the same rule as
`analyses/root_dictionary_test.py`. A label word is a **hit** if its root is one of the four bath roots.

## Tests

- **M1.** Share of hits among label words on Biological pages, against label words on all other pages. One-sided
  Fisher exact test. Pass: p < 0.01. If there are fewer than 5 hits in total, the result is "too few to test".
- **M2 (descriptive).** Within Biological pages: hits on pool/tube labels (Lt) against bathing-figure labels (Ln),
  two-sided Fisher exact, with p reported. The hit words are listed.

---
Amendments (dated, below this line only):
