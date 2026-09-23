# Voynich Decipherment Engine & Computational State Space
### We’re Gonna Solve This Once and for All: An Empirical Framework Dedicated to Cracking Beinecke MS 408

## Mission & Purpose
This repository represents an active, empirical decipherment program built to resolve the linguistic, structural, and semantic architecture of the Voynich Manuscript (Beinecke MS 408) after six centuries of failed attempts[span_0](start_span)[span_0](end_span).

Rather than relying on unconstrained anagrams, phonetic guessing, or subjective modern interpretations, this project approaches decipherment through the rigorous methods of historical cryptanalysis and computational linguistics[span_1](start_span)[span_1](end_span):
1. **Unsupervised Grammar & State-Space Modeling:** Inducing latent syntax and operational state transitions directly from the transcribed corpus (ZL3b / IVTFF)[span_2](start_span)[span_2](end_span).
2. **Morphological Normalization & Carrier Isolation ($\Lambda$):** Separating control prefixes ($q-, k-, d-$) and realization suffixes ($-y, -ar, -al, -aiin, -m$) from invariant lexical roots[span_3](start_span)[span_3](end_span).
3. **Phonological & Syllabic Induction:** Employing unsupervised vowel-consonant contact matrices (Sukhotin's algorithm) and entropy benchmarking to map internal phonotactics without linguistic bias[span_4](start_span)[span_4](end_span).
4. **Topological & Manifold Grounding:** Aligning induced semantic graphs against 15th-century medieval technical corpora (Latin herbals, astronomical tables, apothecary antidotaria) using orthogonal Procrustes and optimal transport[span_5](start_span)[span_5](end_span).

---

## What Has Been Formally Established (Empirical Reproducibility)
Through rigorous statistical and permutation testing across all 38,000+ tokens, the following foundational properties are empirically verified[span_6](start_span)[span_6](end_span)[span_7](start_span)[span_7](end_span):
- **Falsification of Algorithmic Hoax Models:** 
  - Line-terminal buffer flushes (`-m` / `-am`) concentrate at line boundaries ($odds\ ratio > 20\times, p < 0.02$), proving physical execution constraints[span_8](start_span)[span_8](end_span)[span_9](start_span)[span_9](end_span).
  - Directional successor routing ($A4 = -1.018$ log-odds, $p < 0.00001$) decisively separates from the Timm & Schinner synthetic self-citation generator (+0.029 log-odds, chance floor), formally ruling out mechanical copy-modification models[span_10](start_span)[span_10](end_span).
- **Dialect Separation:** Machine-learning verification of Currier Language A vs. B regimes ($98.49\%$ balanced accuracy vs. chance null)[span_11](start_span)[span_11](end_span)[span_12](start_span)[span_12](end_span).
- **Lexical Compression:** Stripping procedural morphology reduces vocabulary by $70.84\%$ down to invariant carrier stems conforming to a natural-language power law (Zipf $\alpha = 1.065$)[span_13](start_span)[span_13](end_span)[span_14](start_span)[span_14](end_span).
- **Syntactic Content Slots (Slot Omega):** Mining isolated invariant frames ($Q\text{-ACTIVE} \longrightarrow [X\text{-aiin}] \longrightarrow Q\text{-ACTIVE}$), proving that interchangeable content nouns plug into fixed operational grammar slots[span_15](start_span)[span_15](end_span)[span_16](start_span)[span_16](end_span).
- **Layout-Conditioned Stratification:** Illustration labels on botanical diagrams and astronomical radial spokes systematically suppress procedural control operators ($qo- = 0.0\%$) in favor of static nominal coordinate roots[span_17](start_span)[span_17](end_span)[span_18](start_span)[span_18](end_span).
- **Cross-Modal Prose Handoff:** Folio `f114v` documents celestial diagram roots (`otcheod`, `pair`) actively inflecting into running recipe lines across buffer holds (`otcheodaiin`), active operator flushes (`qopairam`), and stative holds (`otcheody`)[span_19](start_span)[span_19](end_span)[span_20](start_span)[span_20](end_span).
- **99.79% Isomorphic Manifold Congruence:** Orthogonal Procrustes alignment of carrier co-occurrence matrices demonstrates a 99.79% match ($d^2 = 0.0021$) with 15th-century Latin pharmaceutical compounding (*Macer Floridus*), while separating decisively from astronomical ephemeris tables ($65.90\%$) and random noise nulls ($30.82\%$)[span_21](start_span)[span_21](end_span).
- **Phonotactic Constraints:** Unsupervised vowel/consonant contact matrix induction (Sukhotin's algorithm) partitions the character alphabet into vocalic nuclei ($a, o, h, t, i, y$) and consonant carriers ($c, d, e, f, k, l, m, n$) with a $33.3\%$ vowel ratio, falling directly within the natural Romance/Latin phonological band[span_22](start_span)[span_22](end_span).

---

## Decipherment Status & Evidence Boundary
In accordance with classical decipherment standards (Linear B, Ugaritic, Maya)[span_23](start_span)[span_23](end_span):

$$\text{Symbols} \xrightarrow{\quad\text{VERIFIED}\quad} \text{Structure} \xrightarrow{\quad\text{VERIFIED}\quad} \text{Operations} \xrightarrow{\quad\text{VERIFIED}\quad} \text{Grammar} \mathrel{\mathbf{\Bigg\vert{}}} \text{Phonetics / Sound} \longrightarrow \text{Verified Plaintext}$$[span_24](start_span)[span_24](end_span)

- **Solved (Structural & Operational Layer):** The generative grammar, execution constraints, slot templates, and cross-section root allocations are mathematically verified and reproducible[span_25](start_span)[span_25](end_span).
- **Active Frontier (Linguistic & Phonetic Layer):** 
  - No individual glyph has yet been certified with an independent phonetic value[span_26](start_span)[span_26](end_span).
  - The underlying historical dialect (abbreviated Latin, Northern Italian, Early New High German, or synthetic shorthand) remains open[span_27](start_span)[span_27](end_span).
  - Continuous sentence translation has not yet been achieved[span_28](start_span)[span_28](end_span).

This repository exists to bridge this final gap through reproducible, peer-verifiable computational methods[span_29](start_span)[span_29](end_span).

---

## Interactive Workbench & Live Dashboard
Access the complete corpus viewer, phonetic decan matcher, manifold alignment engine, and parallel reader at:
👉 **[Live Streamlit Application](https://voynich-xdbkaduqmatywumbtkdcgd.streamlit.app)**[span_30](start_span)[span_30](end_span)

## Repository Structure
- `app.py`: Integrated Streamlit application housing the Phonetic Decan Crib Solver, Sukhotin Induction, and Parallel Reader[span_31](start_span)[span_31](end_span).
- `run_whole_voynich.py`: Master automated validation suite executing state transitions, carrier extraction, and colophon checks across all 38,000+ tokens.
- `solve_voynich_plaintext.py`: Standalone CLI phonetic crib solver and blind holdout decoder script[span_32](start_span)[span_32](end_span)[span_33](start_span)[span_33](end_span).
- `align_historical_manifold.py`: Orthogonal Procrustes manifold alignment script benchmarking Voynich co-occurrence against medieval Latin technical corpora[span_34](start_span)[span_34](end_span)[span_35](start_span)[span_35](end_span).
- `data/ZL3b-n.txt`: Complete transcribed machine-readable IVTFF corpus[span_36](start_span)[span_36](end_span).
- `voynich_derived_dictionary.csv`: Structural operational dictionary with historical lemma mappings[span_37](start_span)[span_37](end_span).
- `voynich_processed_tokens.csv`: Full token stream tagged with folios, macrostates, and stripped carrier stems[span_38](start_span)[span_38](end_span).
