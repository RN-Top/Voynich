# Pre-registration: do word parts combine freely (code-like) or under restrictions (language-like)?

Committed 2026-10-03, **before** the test below is run. Amend only below the line at the end.

## Idea

In natural languages a word's beginning strongly limits how it can end, because roots and inflections go together.
In a slot-filling notation or code, beginnings and endings combine much more freely. This compares the Voynich text
with real Latin, measured the same way.

## Texts

- Voynich: ZL3b paragraph text, Currier A and Currier B separately (canonical clean words).
- Latin: the three CLTK Latin Library texts used in `analyses/comparison_fingerprint.py` (Apicius recipes,
  Albertanus 13th c., Bede 8th c.), read with its `latin_words`.
- Control: the Apicius text through that script's `verbose_cipher` (a cipher keeps the language's structure, so it
  should look like Latin).

## Measure

Word tokens of at least 5 letters, with start = first 2 letters and end = last 2 letters. From each text, a random
sample of N tokens, where N is the smallest eligible count among the texts (seed 20261003). Dependence =
(MI(start; end) − mean MI with ends shuffled among the tokens, over 200 shuffles) / min(H(start), H(end)).
0 means free combination; higher means stronger restriction. 95% intervals come from 200 bootstrap resamples.

## Decision

- **Code-like (freer slots):** both Voynich values lie below all three Latin values, with no overlap of the 95%
  intervals.
- **Language-like:** both Voynich values lie within or above the Latin range.
- **Mixed:** otherwise.

---
Amendments (dated, below this line only):

**2026-10-03, corrections after the first run.** Two implementation errors were found. (1) The code used 20
resamples instead of the registered 200. (2) Resampling **with** replacement inflates MI through duplicate tokens,
so every interval lay above its own point estimate. The first run is kept as `output/slots_report_first_run.md`.
Its point estimates were Voynich A 0.073 and B 0.061, against Latin 0.107–0.284. The rerun uses 200 half-samples
**without** replacement (N/2 tokens each) for the intervals. To keep the run time manageable, the shuffle baseline
inside each resample uses 50 shuffles instead of 200 (the point estimates keep the same procedure). The point
estimates, statistic and decision rule are unchanged. Half-sample intervals are wider than full-sample ones, which
makes the "code-like" verdict harder to reach, not easier.
