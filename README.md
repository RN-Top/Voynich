# Voynich Computational Decipherment & State-Space Engine

An automated computational pipeline and interactive research workbench for the structural and lexical analysis of the Voynich Manuscript (Beinecke MS 408).

The framework combines **unsupervised grammar induction**, **PPMI vector space embedding**, **Procrustes manifold alignment**, and a specialized **Author Signature & Scribal Colophon Decipher** module to analyze both primary ciphertext dynamics and historical provenance markers.

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
        ┌───────────────────┼────────────────────┐
        ▼                   ▼                    ▼
┌─────────────────┐ ┌─────────────────┐ ┌──────────────────────┐
│  STATISTICAL    │ │   ASTRONOMICAL  │ │    AUTHOR / COLOPHON │
│   GROUNDING     │ │    ALIGNMENT    │ │       DECIPHER       │
│  (analyzer.py)  │ │  (decoder.py)   │ │(engine_decipher.py)  │
│ - Slot Omega    │ │ - 12 Zodiac Rota│ │ - Colophon (=Pt/+Pc) │
│ - PMI Discovery │ │ - House Bounds  │ │ - Tepenecz & Margins │
│ - Cross-Domain  │ │ - Star Clusters │ │ - Vocabulary Isolation│
└────────┬────────┘ └────────┬────────┘ └──────────┬───────────┘
         │                   │                     │
         └───────────────────┼─────────────────────┘
                             │
                             ▼
┌────────────────────────────────────────────────────────┐
│         COMPUTATIONAL DECIPHERMENT ENGINE              │
│               (engine_decipher.py)                     │
│  - Latent SVD Bigram Grammar Induction (4 Roles)       │
│  - Positive Pointwise Mutual Information (PPMI) Space  │
│  - Grammar-Gated Procrustes Manifold Alignment         │
│  - Aligned Lexicon: Voynich -> Latin Lemma -> English  │
│  - Scribal & Attribution Audit (f1r, f8r, f9r, f116v)  │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│          INTERACTIVE TRANSLATION WORKBENCH             │
│                      (app.py)                          │
│  - Live English Translator & Morphosyntactic Glosser   │
│  - Derived Mathematical Dictionary Key                 │
│  - Author Signature & Terminal Colophon Inspector     │
│  - Full Manuscript Parallel Reader Edition             │
└───────────────────────────┘
