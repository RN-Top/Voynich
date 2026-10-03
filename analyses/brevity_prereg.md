# Pre-registration: do frequent words get shorter (Zipf's law of abbreviation)?

Committed 2026-10-03, **before** the test below is run. Amend only below the line at the end.

## Idea

In human languages, more frequent words tend to be shorter (Zipf's law of abbreviation). In a constructed notation
whose words are assembled from slots, length should depend on the parts used, not on frequency, so the law should be
weaker. This compares the Voynich text with real Latin and an enciphered Latin text.

## Texts

The same as `analyses/slots_prereg.md`: Voynich A and B (ZL3b paragraph text, canonical clean words), three
CLTK Latin texts, and the Apicius text through `verbose_cipher`. From each text, a random sample of N tokens, where N
is the smallest token count among the texts (seed 20261003).

## Measure

Over word types occurring at least 5 times in the sample: Spearman correlation between frequency and length
(letters). The law predicts a negative value; **strength** = −ρ. Intervals: 200 half-samples without replacement
(N/2 tokens each, types with 3+ uses), 2.5–97.5 percentiles. Compare intervals with intervals, not with the full
estimates.

## Decision

- **Notation-like (weaker law):** both Voynich half-sample intervals lie entirely below all three Latin intervals.
- **Language-like:** both Voynich point strengths are at or above the weakest Latin strength.
- **Mixed:** otherwise.

---
Amendments (dated, below this line only):
