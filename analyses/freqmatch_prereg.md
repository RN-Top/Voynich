# Pre-registration: can a letter-for-letter key turn the Voynich into Latin? (frequency match)

Committed 2026-10-03, **before** the test below is run. Amend only below the line at the end.

## Idea

If the Voynich were Latin written with one symbol per letter (simple substitution), some symbol → letter key would
make it Latin-like. The classic attack: start from the frequency-rank key, then improve it by swapping letters to
maximise Latin letter-pair likelihood (hill climbing).

## Latin model

The three CLTK Latin texts from `analyses/comparison_fingerprint.py` (`latin_words`: lowercase, j→i, v→u), with
words joined by a boundary mark. The last 20% of each text is held out. A letter-bigram model is trained on the
first 80% (boundary included, +0.5 smoothing). **Score** = mean log2 probability per character, boundaries included.

## Texts solved

Each is solved with the same procedure: rank-order key, then 5 restarts × 20,000 random swaps, keeping
improvements. The best score is kept.
- **Voynich**, Currier A and B separately (paragraph text, canonical clean words), in two symbol schemes:
  (S1) single EVA characters; (S2) EVA with the common clusters ch, sh, cth, ckh, cph, cfh as single symbols.
  Symbols beyond the number of Latin letters in use (by frequency) are pooled into one "other" symbol.
- **Control (must succeed):** held-out Latin enciphered with a random one-to-one key. The solver must recover at
  least 90% of letter tokens correctly, or the test is uninformative.
- **Floor:** held-out Latin with the letters shuffled within each word (letter frequencies kept, letter order
  destroyed), solved the same way.
- **Ceiling:** the true score of the held-out Latin.

## Decision

For each Voynich text and scheme, position = (best score − floor) / (ceiling − floor).
- **Not simple-substitution Latin** if position < 0.5 for all four (A/B × S1/S2).
- **Consistent with substitution** if position ≥ 0.9 for any.
- **Unclear** otherwise.

For illustration only, the opening line of f1r is shown under the best key.

---
Amendments (dated, below this line only):

**2026-10-03, results.** Control recovered 100% of letters. Voynich positions 0.87–0.94 → formally "CONSISTENT
WITH SUBSTITUTION". Extra checks (labelled) show that the decoded Voynich yields only 10–16% real Latin words (real
Latin 86%; reversed Latin 12%). The letter-pair score was an inadequate criterion. **Conclusion: not simple-
substitution Latin.** Write-up: `output/freqmatch_report.md`.
