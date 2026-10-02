# Validation status

See also [REPLICATION.md](REPLICATION.md) for how an independent group can reproduce every number.

**Update:** code for the hypotheses that were not supported has been moved to [`archive/`](archive/README.md),
and the app now presents only the supported structural results. The tests and their outcomes remain
recorded here.

This file records what currently survives independent testing and what does not.
It follows the independent nine-step review by Juan Gabriel Molina (September 2026)
and a re-run of the key tests on the full corpus with `structural_validation.py`.

Reproduce everything below with:

```bash
pip install -r requirements.txt
python structural_validation.py            # ~15 s; writes output/structural_validation_report.md
```

The full, regenerated numbers are in [`output/structural_validation_report.md`](output/structural_validation_report.md).
The run is seeded, and every figure is computed from `data/ZL3b-n.txt`. Nothing is hard-coded.

## Summary

| Claim | Status | Evidence |
|---|---|---|
| -m / -am tokens prefer physical line ends | **Supported** | 605 of 861 paragraph-text -m/-am tokens are line-final (OR ≈ 20.7). Within-line shuffle p ≈ 5e-5 (20,000 perms). The reviewer's independent sample agrees (OR ≈ 3.4, p ≈ 5e-5). |
| Other endings have positional preferences too | **Supported (new)** | -y and -dy lean line-final (OR ≈ 1.8). -eey, -eedy, -ey, -ol, -or and -edy lean mid-line (OR 0.24–0.48). |
| C→L→P→R order beats a within-line shuffle | Weak | Pair score 0.2216 vs 0.2146, p ≈ 0.002. |
| C→L→P→R carries information beyond Markov structure | **Not supported** | Fails Markov-1 (p ≈ 0.13) and Markov-2 (p ≈ 0.40) twins. The 4-token full-cycle rate falls *below* every null. |
| C→L→P→R is the manuscript's preferred order | Mixed | Ranks #1/24 on the full corpus and on both random folio halves. Ranks #5/24 in Currier A and #2/24 in Currier B. The reviewer's untouched split gave #3/24. |
| Knowing the state predicts the next state | **Not supported** | 0.017 bits/token of information gain; accuracy 31.7% vs 28.3% majority baseline. |
| The published ending→state role map is what the manuscript selects | **Not supported** | Random groupings of the same endings (best of 6 cycles each) score higher than the published map: p ≈ 0.99. |
| Published glosses predict manuscript context | **Not supported** | Glossed tokens fall in the section their meaning predicts 28.1% of the time; shuffled glosses do 26.8% ± 7.0% (p ≈ 0.41). |
| 90.2% blind holdout prediction | **Withdrawn** | See below. |
| 99.79% Macer Floridus manifold congruence | **Withdrawn** | See below. |
| Δ = −1.018 directional routing shift | **Withdrawn / under review** | See below. |
| Venetian / German procedural semantics | Not established | No test in this repository constrains the glosses independently of the morphology they were derived from. |

## Clean blind holdout (added 1 October 2026)

A replacement for the withdrawn 90.2% test. Run it with `python blind_holdout.py`; results are in
[`output/blind_holdout_report.md`](output/blind_holdout_report.md). It is also on the Holdout tab of the app.

- **Holdout:** 43 folios, drawn at random (seed 20261001) from the 216 folios never used for cribs, the
  dossier or the old holdout. The list is in `data/blind_holdout_v1.json`. It was committed on its own,
  before any scoring code existed, and must not be edited.
- **Model:** trained only on the other 184 folios. Its single input is each token's ending under the
  frozen parser rules.
- **Targets:** none of them can be read off the token's own spelling.

| Target | Result | Verdict |
|---|---|---|
| A. Which token ends the line (15 endings) | AUC 0.671 vs 0.501 chance, p ≈ 0.0005 | **PASS** |
| A. Same, using only the 4 states C/L/P/R | AUC 0.581 vs 0.501, p ≈ 0.0005 | **PASS** (weaker) |
| B. Label / diagram text vs paragraph text | AUC 0.635 vs 0.500, p ≈ 0.0005 | **PASS** |
| C. Which section each folio belongs to | 65.1% correct; always guessing "Herbal" also scores 65.1% | **FAIL** |
| D. A token's stem (prefix and ending removed) predicts its ending | 0.775 bits/token better than ignoring the stem, p ≈ 0.001 | **PASS** |

Target D was added later, as Juan's "recurring carrier stems" check. It was committed before its first
run on this holdout. Part of its signal is orthographic (letters next to the ending), so it shows
consistent word-building across pages, not meaning.

The endings carry real, transferable information about line position and page layout on pages the
model never saw. Grouping the endings into the four C/L/P/R states loses about 30% of that
information (0.048 → 0.034 bits per token). This is consistent with the affix-role tournament:
position is carried by individual endings more than by the four-state grouping.

The rule that section prediction must also beat the majority guess was added after the first run.
It is stricter only, and no score changed.

## Transfer to a second representation

`python transfer_test.py` reruns the frozen tests on a second representation of the text: ZL's last
alternative readings, with uncertain spaces not treated as word breaks (36,218 tokens instead of
38,958). Every verdict is unchanged. -m/-am line-end OR is 20.7 vs 20.3; blind A AUC 0.671 vs 0.675;
blind B AUC 0.635 vs 0.644; blind D 0.775 vs 0.744 bits; C→L→P→R still fails the Markov twins.
Details are in [`output/transfer_report.md`](output/transfer_report.md).

This shows the results don't hinge on ZL's editorial choices. It is **not** an independent
transcription. Takahashi's `IT2a-n.txt` (voynich.nu) could not be downloaded from the environment
these tests ran in. Run `python transfer_test.py --corpus IT2a-n.txt`, or upload the file in the
app's sidebar, to complete the external-transfer step.

## Structure-only presentation

Following the advice to strip the model back to what works, the app now shows only the structural results.
The glosses and the four-state presentation have been removed from it; their code is in `archive/`.

## What kind of system? (October 2026)

### Is line-final -m/-am a space-saving device? (pre-registered)

Pre-registration: `analyses/m_abbreviation_prereg.md`, committed before the code
(`analyses/m_abbreviation_test.py`). Report: [`output/m_abbreviation_report.md`](output/m_abbreviation_report.md).

- **Decision under the pre-registered rule: H_space supported.**
- The key result: -m/-am is about **half as common at the end of paragraphs** (8.5% vs 16.1% of
  line-final tokens, p ≈ 1e-4), where the scribe was not short of room. An end-of-unit marker
  ("seal", "finis", "flush") predicts the opposite, so the terminator reading is disfavoured.
- Line-final -m/-am forms are shorter than the same stem's mid-line forms (p ≈ 1e-4). This is
  partly built in, because -am is a short ending.
- Lines ending in -m/-am are **not** measurably fuller (P1 fails), so it is not simply "ran out of room".
- -m/-am words reuse ordinary stems: they are normal words in a line-end form, not a special vocabulary.

Best current reading: **-m/-am is a scribal line-end variant**, used when a line breaks inside running
text and avoided at paragraph ends.

### Comparison with real Latin and a simple cipher (exploratory)

`analyses/comparison_fingerprint.py` applies one generic pipeline (ending = last 2 letters) to Voynich
paragraph text, Latin recipe prose (Apicius), medieval Latin prose (Albertanus, 13th c.; Bede, 8th c.),
and Apicius under a fixed verbose letter cipher. Report:
[`output/comparison_fingerprint_report.md`](output/comparison_fingerprint_report.md).

| | Voynich | Latin texts | Latin, verbose cipher |
|---|---:|---:|---:|
| Strongest line-final ending, odds ratio | **22.9** (-am); **1.8** once the same words are re-lined | 1.7–2.8 | 1.7 |
| Conditional character entropy h2 (bits) | 2.11 | 3.20–3.36 | 2.39 |
| Mean word length | 4.96 | 5.7–6.1 | 11.8 |
| Stem → ending information (bits/word) | 1.35 | 3.5–3.7 | 3.35 |
| Same word twice in a row | 0.84% (0.37% if shuffled) | 0.01–0.21% | 0.21% |

What this suggests:
- The line-end effect **disappears when the Voynich's own words are re-lined**, so it belongs to
  the physical lines of the manuscript. This fits the scribal-convention reading above.
- Voynich characters are far more predictable than Latin letters (low h2). A letter-by-letter cipher
  of Latin moves h2 toward Voynich but makes words more than twice too long, so a simple letter
  cipher of Latin does not fit.
- Voynich endings are much less tied to their stems than Latin inflections are, under this generic
  definition.

Limits: Latin only (Italian or German texts can be dropped into `data/comparison/`); the re-lined
texts have no real manuscript lines; h2 depends on the transcription alphabet. A faithful
implementation of the published Timm & Schinner self-citation algorithm is still needed for a fair
"hoax" comparison. A first, simplified version produced unrealistic text and was removed rather
than tuned.

### Do the two halves of a folded sheet belong together? (pre-registered)

Pre-registration: `analyses/fold_sheets_prereg.md`. Code: `analyses/fold_sheets_test.py`. Report:
[`output/fold_sheets_report.md`](output/fold_sheets_report.md).

The idea, from the project author: folding brings the front, back and center fold together. In a
gathering, leaf k and leaf lo+hi−k are halves of one folded sheet.

- **Pre-registered decision: Supported.** Sheet halves share more vocabulary than random leaf pairs in the
  same gathering: cosine 0.573 vs 0.472, p ≈ 1e-4. This holds even after excluding center-fold
  (adjacent) pairs: 36 sheets.
- **Same scribe and language don't explain it** (exploratory follow-up): 21 of 27 same-scribe,
  same-language sheets, p ≈ 2e-4.
- **No positional line-up.** The same word at the same spot when folded is not significant without
  adjacent pairs (p ≈ 0.015).
- **Reading:** sheets look like units of writing, consistent with the text being written on loose sheets
  before binding. That is useful for reconstructing the original page order. It does **not** show a
  positional key.

### Fold overlay (exploratory)

The idea: fold the front and back pages in toward the center; the words that land on each other form
a key. `archive/pages/12_Fold_Overlay.py` (built on `archive/analyses/fold_overlay.py`, now archived) folds any page onto any other,
mirroring it left-to-right. Positions are approximated from line number and place in the line. It
then folds every other page onto the same target, for a fair comparison.

| Folded page → target | Same word | Same ending | Other pages scoring at least as high |
|---|---:|---:|---|
| f1r → f116r | 0.5% | 8.4% (typical 6.8%) | 30% / 23% |
| f1r → f58r | 0.5% | 13.1% (typical 8.0%) | 10% / 9% |
| f1r → f58v | 0.0% | 12.6% (typical 9.1%) | 100% / 20% |
| f116r → f58r | 0.2% | 6.9% (typical 8.0%) | 18% / 66% |
| f116r → f58v | 0.0% | 7.7% (typical 9.3%) | 100% / 71% |

None of these stand out from ordinary pages. f58r/f58v were used as the center, as the middle of
gathering H (whose central leaves f59–64 are missing). Exact page coordinates from the Beinecke images
would make the overlay more precise than this line-and-word approximation.

### Looking for a key inside the manuscript (October 2026)

**Zodiac labels as day names (pre-registered).** Each sign has 29–30 labelled figures, about one per day.
If the labels name days, the same position on different months should carry the same name.
Pre-registration: `analyses/zodiac_days_prereg.md`. Code: `analyses/zodiac_days_test.py`. Report:
[`output/zodiac_days_report.md`](output/zodiac_days_report.md).
**Decision: Not supported.** Best-rotation positional similarity is 0.123, against 0.125 for shuffled
labels (p = 0.76). Almost all labels start with `o` (`ot-`, `ok-`, `ol-`, `op-`), unlike running text.

**Anomaly scan (exploratory).** `analyses/anomaly_scan.py`, also the app page *Anomaly Scan*. Each page
is compared with pages of the same section and Currier language. Report:
[`output/anomaly_scan_report.md`](output/anomaly_scan_report.md).
- It finds the transcription's key-like pages on its own: **f57v #1** (score 21) and **f49v #9**.
- f1r ranks near the bottom, because its Roman-alphabet "key" is in the margin and is not part of the
  transcribed Voynich text. That needs the page images.
- New candidates: f86v3 and fRos (rosettes), f67r1 (12-sector diagram), f67v2, f17r, f3r, f105v, f116r.

**Key-like sequences.** The f57v ring repeats a 17-symbol cycle four times. The f49v margin column repeats
"p o ● y e ●" twice. Neither contains the most common letters of the running text (e, h, a, c, i), so
neither looks like a complete alphabet for the main script. They read more like lists of special
symbols. f57v and f58r (the transcription suspects a key there too) sit at the center of the book,
beside the missing leaves f59–64.

## Instrument hypothesis (October 2026)

Do the circular diagrams show a measuring instrument (astrolabe/volvelle)? Pre-registered in
`analyses/instrument_prereg.md`, checked against the Yale images. Pointer lines: 1 (needed 3). Centre
pivots: none (needed 2). Labels repeating at the same angular position on non-zodiac circles: p = 0.0195
(needed < 0.01). Rim strokes could not be counted at PDF resolution. **Not supported** under the
pre-registered rule, whatever the rim count. Details: `output/instrument_report.md`.

## Fifth-element cycle (October 2026)

Does the C → L → P → R cycle work if the roleless words (`?`, 14% of paragraph text) are added as a fifth,
"grounding" step? Pre-registered in `analyses/fifth_element_prereg.md`. In every placement, full five-step
runs occur **less** often than in shuffled or Markov text (p = 0.97 and 0.99 against Markov-1 and Markov-2).
**Not supported.** Details: `output/fifth_element_report.md`.

## Alchemy (October 2026)

Do the drawings show the usual marks of an alchemical book? Pre-registered in `analyses/alchemy_prereg.md`;
every page of the Yale images viewed. No fire, stills or alembics (the pool-and-pipe pages f78r, f81r and f83v
are borderline and excluded by the rule). No metal or planet signs. **Not supported.** The pictures fit
herbal, pharmacy, healing-bath and astrology books better. Details: `output/alchemy_report.md`.

## Writing types, word order, topic location (October 2026)

Pre-registered in `analyses/writing_types_prereg.md`. Splitting the text into paragraph A, paragraph B, ring
text, labels and radial text: **word order carries information** beyond line-start/line-end habits in A, B
and ring text (p = 0.001; not caused by repeated words). **Word beginnings track the page's topic more than
endings do** (with the A/B difference removed). **Supported.** Details: `output/writing_types_report.md`.

## Label beginnings vs picture kind (October 2026)

Do labels on different kinds of picture (jars vs plant parts; bathing figures vs pools) start differently, on
the same pages? Pre-registered in `analyses/dictionary_prereg.md`. Neither passed (p = 0.080, 0.34): **not
supported**. Not part of the verdict: jar-label *endings* differ from plant-part-label endings (p = 0.002), a
lead for a follow-up test. Details: `output/dictionary_report.md`.

## Set phrases and grammar links (October 2026)

Pre-registered in `analyses/phrases_prereg.md`. Paragraph text has about 3 times as many strongly bound word
pairs (set phrases) as shuffled text, in both Currier A and B. The strongest link between neighbouring words runs
from a word's **ending** to the next word's **beginning** (e.g. -dy → qok-). This holds whether or not
uncertain spaces are split. **Supported.** Details: `output/phrases_report.md`.

## Implementation problems found and fixed

1. **The live app loaded zero tokens from the corpus.** Every IVTFF text line starts with
   `<f…`, and the old `app.py` loader treated every such line as a folio header, then
   skipped it. So the dashboard's headline figures were all fallback constants: token
   count 0, "69.4%" line flush, "Δ = −1.018", a 20-token hand-typed "holdout", a "30.3%"
   baseline and "p = 0.0000". Even with that fixed, the old loader split on whitespace,
   which would have merged each ZL line into one token, because ZL separates words with
   `.` and `,`.
   *Fix:* `app.py` now loads through the canonical `parser.parse_zl3b` and nothing else.
2. **Numerical fallbacks.** All of them are removed. A value that cannot be computed now
   shows `not computed`. The same applies to the offline sample corpus and the default
   transition, Slot Ω, reader and colophon tables.
3. **Two state maps.** `app.py` had its own macrostate rules. For example, it put `-ol`
   and `-or` in L, while `parser.py` puts `-ol` in P. The app now delegates to `parser.py`.
4. **Parser details.** The `<->` drawing-gap marker was gluing neighbouring words
   together on 627 lines. Line-end flags were also computed before empty tokens were
   dropped. Both are fixed. The parser now records `locus_type` (P / L / C / R), so
   paragraph text can be separated from labels, rings and radii.
5. **Macer Floridus alignment.** `engine_manifold_align.py` (now in `archive/`) built the "historical" target
   vectors with `np.random.randn()`. It also aligned 10 anchors in 16 dimensions, where an
   orthogonal map fits almost any configuration. The resulting 99.79% says nothing about
   Macer Floridus. The module now refuses to run without a real, tokenised target corpus.
   It requires at least 3 anchors per dimension and reports a shuffled-anchor null.
6. **"Semantic" and "affix-role" tournaments in the app.** Both used to compute bigram
   mutual information of tokens (or prefix+suffix strings) against a global shuffle,
   which tests neither semantics nor the role map. They now run tests 6 and 5 of
   `structural_validation.py`.

## Withdrawn headline claims

- **90.2% blind prediction (394/437).** The five holdout folios (`f70v2`, `f71r`, `f72r1`,
  `f72v1`, `f72v2`) are also in `blind_test.SEEN_FOLIOS`, the folios already used for the
  dossier. The score also compares `predict_apparatus_role` with `get_expected_role`, and
  both are suffix rules applied to the same token string. That measures how much two rule
  sets overlap, not prediction of independent ground truth. On the real tokens of those
  folios the agreement is 70.6% (538 tokens) against a 31.6% label-shuffle baseline. A
  clean replacement needs a new holdout, chosen and frozen before any rules are adjusted.
- **99.79% Macer Floridus congruence.** It came from random target geometry (see item 5
  above). To rebuild it, supply a real Macer Floridus transcription to
  `CrossLingualManifoldAligner.run_alignment_benchmark`.
- **Δ = −1.018.** This was the fallback constant shown when the loader returned no data.
  The same formula on correctly parsed tokens gives **Δ ≈ +1.50**: `-al` is *more* likely
  than `-ar` to be followed by a `k-`/`d-` token, which is the opposite sign. Any claim
  built on the sign of this shift, including the "hoax falsified" framing, needs to be
  re-derived.

## What looks real

The morphology-plus-position layer holds up. Voynich endings are not distributed
randomly with respect to the physical line, and -m/-am is the strongest case by a wide
margin. The literature has noted a line-final preference for `m` before, so this confirms
the parser captures a real property of the text. It is not by itself evidence for any
reading of it.

## Suggested next steps

1. Keep the structural layer frozen and meaning-free. Diagram vs prose, line position and carrier
   stems now pass on blind folios; section does not. **Still open:** an independent transcription
   (Takahashi `IT2a-n.txt`; see REPLICATION.md) and Currier hand as a target.
2. ~~Pre-register a new holdout~~ Done: `data/blind_holdout_v1.json` (see above). For the next rule
   version, draw a fresh holdout (v2) rather than reusing v1.
3. Rebuild the semantic layer only on top of targets the glosses make *different*
   predictions for. Then re-run the semantic permutation tournament. If the published
   glosses win decisively there, that result would matter.
4. Try ending-level position models (per-ending line-final rates) before four-state
   machines. The per-ending table suggests position is carried by individual endings
   more than by the C/L/P/R grouping.
