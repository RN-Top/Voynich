# Pre-registration: do the Voynich symbols alternate like vowels and consonants? (Sukhotin)

Committed 2026-10-03, **before** the test below is run. Amend only below the line at the end.

## Idea

Phonetic alphabets show vowel/consonant alternation. Sukhotin's algorithm finds a vowel set from a text alone:
build the symmetric matrix of adjacent-letter counts within words (diagonal set to zero); repeatedly mark as vowel
the unmarked letter with the largest positive remaining row sum, then subtract 2 × its adjacency from the other
letters' sums; stop when no positive sum remains.

## Measure

Alternation = share of within-word adjacent letter pairs that are vowel–consonant or consonant–vowel under the
found split. Each text is compared with itself with letters shuffled within each word (Sukhotin rerun on the
shuffled text; mean of 20 shuffles, seed 20261003). **Excess** = real alternation − shuffled alternation.

## Texts

- **Latin (control):** the three CLTK texts (latin_words; first 100,000 words). Sukhotin must mark at least 4 of
  a, e, i, o, u as vowels, or the method is uninformative.
- **Voynich**, Currier A and B, paragraph text, in two symbol schemes: S1 single EVA characters, and S2 with ch, sh,
  cth, ckh, cph, cfh as single symbols.

## Decision

Ratio = Voynich excess / Latin excess, for each of the four Voynich cases.
- **Alphabet-like** if the ratio ≥ 0.5 in all four.
- **Not alphabet-like** if the ratio < 0.5 in all four.
- **Mixed** otherwise.

The vowel sets found are reported.

---
Amendments (dated, below this line only):
