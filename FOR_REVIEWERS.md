# For reviewers: how to check this work

Thank you for looking. This page lists the results worth checking first, with the files and the one command that
reruns each one. Every test here was **pre-registered**: the prediction, the comparison and the pass rule were
committed before the test was first run, and failures are reported alongside passes.

Nothing in this repository claims a decipherment. An earlier "alchemical recipe" reading (17 November 2026) was
withdrawn; see [`retracted/README.md`](retracted/README.md) for why.

## Setup

Python 3, standard library only for the tests below. Clone the repository and run from its top folder.

## 1. Plant-page openings share rare spellings with star labels (supported)

- Prediction, written first: [`analyses/plant_star_prereg.md`](analyses/plant_star_prereg.md), re-run plan
  [`analyses/rerun_integrated_prereg.md`](analyses/rerun_integrated_prereg.md)
- Result: [`output/plant_star_report_integrated.md`](output/plant_star_report_integrated.md),
  summary [`output/rerun_integrated_report.md`](output/rerun_integrated_report.md)
- Rerun: `python3 analyses/rerun_with_integrated.py` (about 30 seconds)

14 of 128 herbal-page opening words share an unusual letter chunk with the star labels on f67r2 and f68r1–3,
against 4.5 expected when the same number of words is drawn from other labels (10,000 draws, p = 0.0001). It
survives Holm correction across the five decisions in that re-run. Examples: *koaiin* (f3v) ~ *okoaly* (f68r1),
*pocheody* (f16r) ~ *opocphor* (f68r2), *tydlo* (f9r) ~ *otydy* (f68r1).

What to check: whether drawing the comparison words from other labels is a fair control, and whether a few shared
chunks involve rare glyphs written as `@nnn;` codes in ZL3b (e.g. `c@133h`), which may deserve separate handling.

## 2. Fontana's cipher methods do not decode the text (not supported)

- Prediction, written first: [`analyses/fontana_cipher_prereg.md`](analyses/fontana_cipher_prereg.md)
- Result: [`output/fontana_cipher_report.md`](output/fontana_cipher_report.md)
- Rerun: `python3 analyses/fontana_cipher_decoder.py` (seed 1453; takes a while)

36 substitution variants (one or several signs per letter; forwards, word-reversed or mirrored; EVA letters or
letter groups; Latin, Italian, Venetian), each solved on half the pages and scored on the other half. The same
solver recovers real Latin and Italian put through the same ciphers at 94–100% real words, so the method works.
On the Voynich no variant passes. This rules out *simple* Fontana-style substitution, not Fontana as author, and not
abbreviation systems, nulls, code-books or other languages.

## 3. Other pre-registered tests

All in [`analyses/`](analyses/) (prediction) and [`output/`](output/) (result), summarised in
[`VALIDATION.md`](VALIDATION.md):

- Reading direction, line by line and whole file: no preference for backwards
  (`backwards_test.py`, `whole_file_direction_test.py`)
- Herb → star → body/remedy chains: not supported (`chains_test.py`)
- Labels appearing in their own page's text: not supported (`ground_test.py`)

The chains test reruns with tiny differences in expected counts (e.g. 5.52 vs 5.53); the verdicts do not change.

## 4. The data

- [`voynich_integrated.json`](voynich_integrated.json): every page in book order with its ZL3b text, labels, drawing
  type and Yale photo link(s); 227 pages and panels, about 39,000 words.
- [`voynich_control.json`](voynich_control.json): the same pages with words shuffled across pages, as a negative
  control. Any pattern claimed on the real file should be checked on this one too.

## Feedback

Erin Rae Toppe, raenova060@gmail.com. Corrections, failed reruns and better controls are all welcome.
