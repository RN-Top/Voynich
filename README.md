# Voynich Computational Decipherment & State-Space Engine

An automated, reproducible computational pipeline and interactive workbench for the Voynich Manuscript (Beinecke MS 408).

The project bypasses arbitrary anagramming and subjective glossing by combining **unsupervised grammar induction**, **PPMI vector space embedding**, and **manifold alignment** against 15th-century medieval technical corpora.

---

## 1. System Pipeline Architecture

Surface tokens decompose through a parameterized instruction framework:

$$\text{Surface Token } W = \mathcal{C}\big([\Lambda \times N_E \times O_I] + \rho\big)$$

```text
┌────────────────────────────────────────────────────────┐
│               RAW TRANSLITERATION CORPUS               │
│                     (data/ZL3b-n.txt)                  │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│           MORPHOTACTIC TOKENIZER & PARSER              │
│                     (parser.py)                        │
│  - Strips Control Headers C in {q, k, d}               │
│  - Isolates Invariant Carrier Cores (Lambda)           │
│  - Tracks Successor Realization Ports rho in {al, ar}  │
│  - Enforces terminal line flushes (A2: terminal -m)    │
└───────────────────────────┬────────────────────────────┘
                            │
        ┌───────────────────┴────────────────────┐
        ▼                                        ▼
┌──────────────────────────────┐ ┌──────────────────────────────┐
│     STATISTICAL GROUNDING    │ │    ASTRONOMICAL ALIGNMENT    │
│        (analyzer.py)         │ │        (decoder.py)          │
│ - Slot Omega Syntactic Mining│ │ - 12 Zodiac House Invariance │
│ - Pointwise Mutual Info (PMI)│ │ - Clock/Rota Positional Map  │
│ - Cross-Modal Domain Entropy │ │ - Celestial Label Matrix     │
└──────────────┬───────────────┘ └──────────────┬───────────────┘
               │                                │
               └────────────────┬───────────────┘
                                │
                                ▼
┌────────────────────────────────────────────────────────┐
│         COMPUTATIONAL DECIPHERMENT ENGINE              │
│               (engine_decipher.py)                     │
│  - Latent SVD Bigram Grammar Induction (4 Roles)       │
│  - Positive Pointwise Mutual Information (PPMI) Space  │
│  - Grammar-Gated Procrustes Manifold Alignment         │
│  - Aligned Lexicon: Voynich -> Latin Lemma -> English  │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│          INTERACTIVE TRANSLATION WORKBENCH             │
│                      (app.py)                          │
│  - Live English Translator & Morphosyntactic Glosser   │
│  - Derived Mathematical Dictionary Key                 │
│  - Syntactic Category Distribution Viewer              │
│  - Full Manuscript Parallel Reader Edition             │
└────────────────────────────────────────────────────────┘
