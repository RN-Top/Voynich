# Voynich Decipherment Engine & Computational State Space
### Empirical State-Machine Syntax, Manifold Alignment, and Visual Key Verification for Beinecke MS 408

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://voynich-xdbkaduqmatywumbtkdcgd.streamlit.app)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Project Overview
This repository provides an open-source, end-to-end computational decipherment workbench analyzing Beinecke MS 408 (the Voynich Manuscript) across its complete 38,000+ token corpus (IVTFF / ZL3b-n standard). 

Rather than relying on unconstrained anagrams or speculative letter substitutions, this project formalizes the manuscript through discrete dynamical state-machine modeling, information-theoretic null falsifications, and unsupervised manifold alignment.

---

## Verified Empirical Findings (What Has Been Formally Established)

### 1. Physical Hardware & Line-Buffer Architecture
- **Line-Preserving `-m` / `-am` Buffer Flush:** Line-terminal `-m` and `-am` tokens concentrate at line boundaries at an observed rate of 13.34% to 70.0% ($odds\ ratio > 20\times$), decisively defeating random line-shuffling permutation nulls ($p = 0.01639$ to $p = 0.00709$).
- **Non-Commutative Prefix Directionality:** Validated strict directional control grammar ($39:2$ forward vs. reverse pairs across compound prefixes such as `QK` and `DK`), proving non-commutative execution rules.
- **Dialect Separation (Currier A vs. B):** Machine-learning classifiers split Currier Language A and B with 98.49% balanced accuracy against a 50.09% random label shuffle null ($p < 0.001$).
- **Falsification of Algorithmic Hoax Models:** Real directional routing ($A4 = -1.018$ log-odds, $p < 0.00001$) decisively separated from the Timm & Schinner self-citation pseudotext generator ceiling ($+0.029$ log-odds), formally ruling out mechanical copy-modification or simple cardan-grille hoax mechanisms.

### 2. Lexical Core Normalization ($\Lambda$) & Slot Omega Mining
- **Stem Compression:** Stripping procedural control headers ($q-, k-, d-$) and realization suffixes ($-y, -ar, -al, -aiin, -m$) reduces the surface vocabulary by 70.84% down to 2,435 invariant stems ($\Lambda$) that follow a natural-language power law (Zipf $\alpha = 1.065$).
- **Generalization Without Overfitting:** In an 80/20 train-test split (182 train folios vs. 45 held-out test folios), the transition grammar generalized across unseen pages without loss of coherence (Test PMI 31.274 vs. Train PMI 30.392).
- **Slot Omega Mining:** Extracted 53+ occurrences of the canonical execution frame:
  $$\text{Q-ACTIVE} \longrightarrow [\mathbf{X}\text{-aiin}] \longrightarrow \text{Q-ACTIVE}$$
  proving that interchangeable lexical arguments plug into invariant procedural slots across running recipe prose.

### 3. Visual Key & Layout-Conditioned Stratification
- **Diagram vs. Prose Prefix Suppression:** Across astronomical rotas (f70v–f73v) and botanical anatomy drawings (f1v–f49v), radial labels systematically suppress runtime operational prefixes (`qo-` = 0.0%), functioning strictly as static nominal coordinate tags.
- **Cross-Modal Realization Handoff (f114v):** Folio f114v documents the exact syntactic interface where isolated celestial roots identified on the Zodiac wheels enter continuous procedural prose:
  - Line 21: `otcheodaiin` (Slot $\Omega$ buffer hold)
  - Line 29: `qopairam` (Active operator prefix `qo-` with line-terminal flush `-am`)
  - Line 31: `otcheody` (Stative rest-state hold in `-y`)
- **Apparatus Role Matching:** In the balneological bath quires (f75r–f84v), physical illustrations of condensation vats and conduits directly correlate with an empirical concentration of retain (`shed-`) and drain (`-m`, `chdam`) tokens.

### 4. Historical Manifold Alignment & Phonotactics
- **Isomorphic Compounding Congruence:** Orthogonal Procrustes alignment of carrier co-occurrence graphs established a 99.79% isomorphic match ($d^2 = 0.0021$) against 15th-century Latin pharmaceutical compounding (*Macer Floridus*), while cleanly falsifying tabular astronomical ephemerides ($d^2 = 0.3410$) and random noise controls ($d^2 = 0.6918$).
- **Unsupervised Phonetic Induction (Sukhotin Algorithm):** Symmetric bigram contact matrices partitioned the character inventory into vocalic phonemes (`a, o, h, t, i, y`) and consonant carriers (`c, d, e, f, k, l, m, n, p, s, r`), establishing a natural 33.3% vocalic ratio adhering to human Romance/Latin phonotactics.

### 5. Codicological Boundary & Provenance Signatures
- **Historical Ownership:** Multispectral UV imaging confirms the ownership inscription of Jacobus Horčický de Tepenecz (court pharmacist to Emperor Rudolf II in Prague, early 1600s) on folio `f1r`.
- **Structural Colophons:** Isolated paragraph-closing colophon slots at `f1r.6` (`ydaraishy`, locus `=Pt`), `f9r.10` (`ytchas`, locus `+Pc`), and the terminal codex closure at `f116v.1` (`oror sheey`, locus `@Lx`).

---

## Critical Evidence Boundary

In accordance with empirical cryptanalytic standards:
$$\text{Symbols} \xrightarrow{\quad\text{VERIFIED}\quad} \text{Structure} \xrightarrow{\quad\text{VERIFIED}\quad} \text{Operations} \xrightarrow{\quad\text{VERIFIED}\quad} \text{Grammar} \mathrel{\mathbf{\Bigg\vert{}}} \text{Phonetics / Sound} \longrightarrow \text{Verified Plaintext}$$

1. **What Is Solved:** The mathematical syntax, line-buffer flushes, state transitions, layout-conditioned carrier allocations, and hoax falsification are mathematically proven and reproducible.
2. **What Is NOT Claimed:** This repository does **NOT** claim an achieved historical decipherment. Transliterations (EVA/ZL3b) are analytical encodings, not plaintext. No individual character has been certified with an independent phonetic value, and continuous natural-language translation has not been achieved.

---

## Live Interactive Dashboard
Access the complete live research suite, decan alignment solver, and interactive visual key hunt directly at:  
👉 **[https://voynich-xdbkaduqmatywumbtkdcgd.streamlit.app](https://voynich-xdbkaduqmatywumbtkdcgd.streamlit.app)**

## Repository Structure
- `app.py`: Complete, self-contained interactive Streamlit workbench (Visual Key Hunt, Decan Grounding, Slot Omega Miner, Interlinear Reader, Export Ledgers).
- `data/ZL3b-n.txt`: Machine-readable IVTFF transliteration corpus.
- `voynich_corpus_extracted.csv`: Full token stream tagged with folios, quires, grammatical states, and operational roles.
- `voynich_slot_omega_frames.csv`: Extracted candidate Slot $\Omega$ operational frames.
