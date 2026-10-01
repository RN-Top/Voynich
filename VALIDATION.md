# Validation status

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

The endings carry real, transferable information about line position and page layout on pages the
model never saw. Grouping the endings into the four C/L/P/R states loses about 30% of that
information (0.048 → 0.034 bits per token). This is consistent with the affix-role tournament:
position is carried by individual endings more than by the four-state grouping.

The rule that section prediction must also beat the majority guess was added after the first run.
It is stricter only, and no score changed.

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
5. **Macer Floridus alignment.** `engine_manifold_align.py` built the "historical" target
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

1. Keep the structural layer frozen and meaning-free. Add targets for it to predict:
   section, diagram vs prose, Currier hand, and a second transcription (for example
   Takahashi or the v101 transliteration) for external transfer.
2. ~~Pre-register a new holdout~~ Done: `data/blind_holdout_v1.json` (see above). For the next rule
   version, draw a fresh holdout (v2) rather than reusing v1.
3. Rebuild the semantic layer only on top of targets the glosses make *different*
   predictions for. Then re-run the semantic permutation tournament. If the published
   glosses win decisively there, that result would matter.
4. Try ending-level position models (per-ending line-final rates) before four-state
   machines. The per-ending table suggests position is carried by individual endings
   more than by the C/L/P/R grouping.
