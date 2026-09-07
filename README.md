# Voynich
# Voynich State Viewer & Morphotactic Engine

An empirical computational workbench and interactive visualization dashboard exploring the Voynich Manuscript (Beinecke MS 408) as an operational state machine, discrete dynamical system, and information-routing network[span_0](start_span)[span_0](end_span)[span_1](start_span)[span_1](end_span).

---

## 1. What This Is

This repository models Voynichese not as an enciphered natural-language prose narrative or simple substitution cipher, but as a constrained generative architecture and state transition pipeline[span_2](start_span)[span_2](end_span)[span_3](start_span)[span_3](end_span).

It parses the authoritative IVTFF transliteration corpus (`ZL3b-n.txt`), extracts morphological feature bundles, maps sequential trajectories across operational macrostates, and renders color-coded token timelines and empirical transition matrices[span_4](start_span)[span_4](end_span)[span_5](start_span)[span_5](end_span)[span_6](start_span)[span_6](end_span).

### The Four-Macrostate Model ($C \to L \to P \to R$)
Tokens are classified into four primary functional regimes based on their terminal morphology and distributional behavior[span_7](start_span)[span_7](end_span)[span_8](start_span)[span_8](end_span):

| State | Candidate Label | Representative Morphology | Systems Architecture Role |
| :---: | :--- | :--- | :--- |
| **`C`** | **Transform** | `-ey`, `-eey`, `-edy`, `-eedy` | Active compute/loop register; feeds forward into $Q$-control[span_9](start_span)[span_9](end_span)[span_10](start_span)[span_10](end_span). |
| **`L`** | **Connect** | `-ain`, `-aiin`, `-or`, `-ar` | Bus/junction state; parameterizes transfers between registers[span_11](start_span)[span_11](end_span)[span_12](start_span)[span_12](end_span). |
| **`P`** | **Maintain** | `-y`, `-ol`, `-al` | Stative register hold; stabilizes state across executions[span_13](start_span)[span_13](end_span)[span_14](start_span)[span_14](end_span). |
| **`R`** | **Resolve** | `-am`, `-m` | Terminal buffer flush; highest line-end association[span_15](start_span)[span_15](end_span)[span_16](start_span)[span_16](end_span). |
| **`?`** | **Unmapped** | Residual / non-conforming | Tokens outside the primary morphological classes[span_17](start_span)[span_17](end_span). |

---

## 2. Core Morphotactic Architecture

Surface tokens are factorized through the empirical v4.0–v6.0 structural pipeline[span_18](start_span)[span_18](end_span)[span_19](start_span)[span_19](end_span):

$$W = \mathcal{C}\big([\Lambda \times N_E \times O_I] + \rho\big)$$[span_20](start_span)[span_20](end_span)

* **$\mathcal{C}$ (Control Header):** Positional and frame-entry operators ($D, Q, K$)[span_21](start_span)[span_21](end_span)[span_22](start_span)[span_22](end_span). $D$ exhibits massive line-initial odds (entry/reset)[span_23](start_span)[span_23](end_span)[span_24](start_span)[span_24](end_span), while outer compound prefixes ($QK, DK$) are ordered and non-commutative[span_25](start_span)[span_25](end_span)[span_26](start_span)[span_26](end_span).
* **$\Lambda$ (Carrier Kernel):** Conserved lexical stems carrying domain/register specificity ($OTCHEOD, CH, PCH, T, OT$)[span_27](start_span)[span_27](end_span)[span_28](start_span)[span_28](end_span).
* **$N_E \times O_I$ (Internal Tuning Registers):** Ordered $E$-multiplicity ($E^0$ to $E^3$) and internal $O$-presence/absence flags[span_29](start_span)[span_29](end_span)[span_30](start_span)[span_30](end_span).
* **$\rho$ (Exit Port / Successor Router):** Realization interfaces ($\{y, ar, al, aiin, m\}$) that govern the control state of the following token[span_31](start_span)[span_31](end_span)[span_32](start_span)[span_32](end_span):
  * **$-m$ / $-am$ (A2 Effect):** Rigid line-terminal bound (~69–73% line-end odds, odds ratio >20x) acting as a buffer flush[span_33](start_span)[span_33](end_span)[span_34](start_span)[span_34](end_span).
  * **$-l$ vs. $-r$ (A4 Effect):** Successor-routing switch; holding the carrier fixed, $-al$ enriches transitions to next-token $K$ and $D$ headers relative to $-ar$[span_35](start_span)[span_35](end_span)[span_36](start_span)[span_36](end_span).
  * **$-y$:** Dedicated handoff interface licensing reentry into $Q$-dominated subroutines[span_37](start_span)[span_37](end_span)[span_38](start_span)[span_38](end_span).

---

## 3. Evidence Boundary & Methodological Rules

1. **Transliteration $\neq$ Plaintext:** EVA, ZL3b, and RF1b are transcription formats, not decoded historical text[span_39](start_span)[span_39](end_span).
2. **Functional Labels $\neq$ Historical Translations:** Labels such as `TRANSFORM`, `CONNECT`, and `RESOLVE` represent observed mathematical and distributional properties, not literal English meanings[span_40](start_span)[span_40](end_span)[span_41](start_span)[span_41](end_span).
3. **Lexical Stop Rule:** Visible carrier cores are not decomposed into subparts unless matched alternations statistically justify segmentation[span_42](start_span)[span_42](end_span).
4. **Falsification First:** Discoveries are benchmarked against line-preserving permutations, Currier-mode controls, and generative nulls (e.g., Timm & Schinner self-citation models)[span_43](start_span)[span_43](end_span).
5. **Decipherment Status:** This is an active structural analysis framework. No complete natural language, secure phonetic mapping, or continuous sentence translation is claimed[span_44](start_span)[span_44](end_span)[span_45](start_span)[span_45](end_span).

---

## 4. Repository Structure

```text
├── app.py                     # Interactive Streamlit dashboard
├── parser.py                  # IVTFF parser, token decomposition, and state mapping
├── test_system.py             # Automated unit tests for morphological factorization
├── requirements.txt           # Python dependencies
├── README.md                  # Project documentation
└── data/
    └── ZL3b-n.txt             # Primary IVTFF transliteration corpus

