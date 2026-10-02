# Archive

Code and documents for hypotheses that were **tested and not supported**, plus earlier engines that the
current validation scripts replace. They are kept so the history is transparent and so any idea can be
revisited if new evidence appears. Nothing here is used by the live app.

| What | Files | Why archived |
|---|---|---|
| Venetian / German translations | `lexicon.py`, `translate_voynich_dialects.py`, `engine_decipher.py`, `decoder.py`, `solve_voynich_plaintext.py`, `run_phonetic_pipeline.py`, `break_phonetic_cribs.py`, `voynich_vault_solver.py` | Glosses do not beat shuffled glosses (semantic permutation test, p ≈ 0.4). `lexicon.py` is still imported by `structural_validation.py` so that test can be rerun. |
| C → L → P → R cycle | `run_whole_voynich.py`, `test_whole_voynich.py`, `src/architecture_contract.py`, `pages/09_Architecture_Contract.py`, `pages/11_Full_Corpus_Counts.py` | Not better than Markov controls; the published role map is not selected. |
| Fold overlay key | `analyses/fold_overlay.py`, `pages/12_Fold_Overlay.py` | Fold overlays match no better than ordinary pages. |
| Zodiac decoding | `zodiac_recipe_decoder.py`, `zodiac_positional_crib.py`, `solve_zodiac_radial.py` | Zodiac labels as day names not supported (p ≈ 0.76). The test itself stays in `analyses/`. |
| Withdrawn headline numbers | `validator.py`, `engine_manifold_align.py`, `align_historical_manifold.py`, `generate_evidence_pdf.py`, `test_voynich_pipeline.py` | 90.2% holdout (pages already used), 99.79% Macer (random vectors), 33.3% vowel ratio (internally inconsistent). |
| Superseded audits | `analyzer.py`, `audit_generator_null.py`, `audit_permutations.py`, `voynich_syntax.zip` | Replaced by `structural_validation.py`, `blind_holdout.py` and `transfer_test.py`. |
| Original README | `ORIGINAL_README.md` | Kept for the record. |
