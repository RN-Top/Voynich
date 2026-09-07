# Voynich State Viewer & Astronomical Decipherment Engine

An empirical computational workbench, morphotactic state-space parser, and cross-modal decipherment engine for the Voynich Manuscript (Beinecke MS 408)[span_2](start_span)[span_2](end_span)[span_3](start_span)[span_3](end_span).

---

## 1. What This Repository Does

Rather than treating Voynichese as an enciphered natural-language narrative or an arbitrary letter-substitution cipher, this project investigates the manuscript as a **discrete dynamical state machine and information-routing architecture**[span_4](start_span)[span_4](end_span):

$$\text{Surface Token } W = \mathcal{C}\big([\Lambda \times N_E \times O_I] + \rho\big)$$[span_5](start_span)[span_5](end_span)

By stripping operational control headers ($\mathcal{C} \in \{Q, K, D\}$) and exit realization ports ($\rho \in \{Y, AR, AL, AIIN, M\}$), the engine isolates **invariant lexical carrier stems ($\Lambda$)**[span_6](start_span)[span_6](end_span). These carrier kernels are then aligned directly with manuscript domain metadata, illustrated zodiac rotas (`f70r`–`f74v`), and syntactic content frames (Slot Omega) without assigning speculative English prose[span_7](start_span)[span_7](end_span)[span_8](start_span)[span_8](end_span).

---

## 2. Theoretical Architecture

### The Four Macrostate Regimes ($C \to L \to P \to R$)
Tokens are classified into four operational states based on terminal morphology and forward transition dynamics[span_9](start_span)[span_9](end_span)[span_10](start_span)[span_10](end_span):

| State | Analytical Label | Representative Morphology | Systems Architecture Role |
| :---: | :--- | :--- | :--- |
| **`C`** | **Transform** | `-ey`, `-eey`, `-edy`, `-eedy` | Active compute/loop register; forward-feeds into $Q$-control[span_11](start_span)[span_11](end_span)[span_12](start_span)[span_12](end_span). |
| **`L`** | **Connect** | `-ain`, `-aiin`, `-or`, `-ar` | Bus/junction state; parameterizes transfers between registers[span_13](start_span)[span_13](end_span)[span_14](start_span)[span_14](end_span). |
| **`P`** | **Maintain** | `-y`, `-ol`, `-al` | Stative register hold; preserves context across execution frames[span_15](start_span)[span_15](end_span)[span_16](start_span)[span_16](end_span). |
| **`R`** | **Resolve** | `-am`, `-m` | Line-terminal buffer flush; rigid execution boundary[span_17](start_span)[span_17](end_span)[span_18](start_span)[span_18](end_span). |
| **`?`** | **Unmapped** | Residual / non-conforming | Tokens outside the primary morphological classes[span_19](start_span)[span_19](end_span). |

### Factorized Token Morphology
Every surface word decomposes into functional layers[span_20](start_span)[span_20](end_span):
* **Control Headers ($\mathcal{C}$):** Positional and frame-entry operators ($D, Q, K$)[span_21](start_span)[span_21](end_span). $D$ exhibits massive line-initial odds (entry/reset)[span_22](start_span)[span_22](end_span), while outer compound prefixes ($QK, DK$) are ordered and non-commutative[span_23](start_span)[span_23](end_span).
* **Carrier Kernels ($\Lambda$):** Stable lexical stems carrying domain and register specificity (`OTCHEOD`, `OEEOD`, `OPAIR`, `OTEOD`, `CH`, `PCH`)[span_24](start_span)[span_24](end_span).
* **Internal Registers ($N_E \times O_I$):** Ordered $E$-multiplicity ($E^0$ to $E^3$) and internal $O$-presence/absence flags[span_25](start_span)[span_25](end_span).
* **Exit Ports / Successor Routers ($\rho$):** Realization interfaces ($\{y, ar, al, aiin, m\}$) parameterizing downstream token selection ($B_n = (\rho_n \to \mathcal{C}_{n+1})$)[span_26](start_span)[span_26](end_span):
  * **$-m$ / $-am$ (A2 Effect):** Terminal flush behavior (~70%+ line-final odds, odds ratio >20x)[span_27](start_span)[span_27](end_span).
  * **$-l$ vs. $-r$ (A4 Effect):** Successor-routing switch; holding the carrier fixed, $-al$ enriches transitions to next-token $K$ and $D$ headers relative to $-ar$[span_28](start_span)[span_28](end_span).
  * **$-y$:** Handoff interface licensing reentry into $Q$-dominated subroutines[span_29](start_span)[span_29](end_span).

---

## 3. Evidence Boundary & Methodological Constraints

To ensure scientific reproducibility, this repository enforces strict research boundaries[span_30](start_span)[span_30](end_span)[span_31](start_span)[span_31](end_span):
1. **Transliteration $\neq$ Plaintext:** EVA, ZL3b, and RF1b are transcription formats, never plaintext language[span_32](start_span)[span_32](end_span)[span_33](start_span)[span_33](end_span).
2. **Functional Labels $\neq$ Historical Plaintext:** Terms like `TRANSFORM`, `CONNECT`, and `RESOLVE` identify mathematical/distributional properties, not literal English translations[span_34](start_span)[span_34](end_span)[span_35](start_span)[span_35](end_span).
3. **Lexical Stop Rule:** Invariant carrier cores are not segmented into individual letters unless matched alternations statistically justify the split[span_36](start_span)[span_36](end_span).
4. **Falsification First:** Morphological models are tested against line-preserving permutations, Currier A/B controls, and generative nulls (such as Timm & Schinner's self-citation generator)[span_37](start_span)[span_37](end_span).
5. **Decipherment Status:** Structural syntax and morphotactics are substantially developed; exact semantics, phonology, and continuous sentence translations remain unverified[span_38](start_span)[span_38](end_span)[span_39](start_span)[span_39](end_span).

---

## 4. Repository Structure

```text
voynich-state-viewer/
├── data/
│   └── ZL3b-n.txt        # Authoritative IVTFF transliteration corpus
├── .gitignore            # Git ignore configurations
├── README.md             # Project documentation and architectural manifest
├── analyzer.py           # Statistical grounding, PMI, and Slot Omega discovery
├── app.py                # Interactive Streamlit exploration & decipherment dashboard
├── decoder.py            # Astronomical alignment oracle & zodiac rota decoding
├── parser.py             # Grounded morphotactic tokenizer and carrier isolator
└── requirements.txt      # Python runtime dependencies
